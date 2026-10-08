"""Cross-client regression tests for the VIGIAFAST inbox access boundary.

All entities here are synthetic. These tests exercise a key belonging to
workspace A against another workspace in the SAME organization (B) and a
workspace in a DIFFERENT organization (C), covering REST, MCP and HTMX.
They do not constitute a full multi-tenant security audit.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.test import Client
from django.utils import timezone

from apps.accounts.models import User
from apps.api_keys import services
from apps.inbox.models import InboxMessage, InboxReply
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.social_accounts.models import SocialAccount
from apps.workspaces.models import Workspace


class _SecureClient(Client):
    def generic(self, method, path, *args, **kwargs):
        kwargs["secure"] = True
        return super().generic(method, path, *args, **kwargs)


@pytest.fixture
def clients(db):
    user = User.objects.create_user(
        email="operator-isolation@example.test",
        password="testpasswordonly",
        name="Test Operator",
        tos_accepted_at=timezone.now(),
    )
    agency = Organization.objects.create(name="Synthetic Agency")
    other_org = Organization.objects.create(name="Synthetic Foreign Organization")
    ws_a = Workspace.objects.create(name="Client A", organization=agency)
    ws_b = Workspace.objects.create(name="Client B", organization=agency)
    ws_c = Workspace.objects.create(name="Client C", organization=other_org)

    OrgMembership.objects.create(
        user=user, organization=agency, org_role=OrgMembership.OrgRole.OWNER
    )
    WorkspaceMembership.objects.create(
        user=user,
        workspace=ws_a,
        workspace_role=WorkspaceMembership.WorkspaceRole.OWNER,
    )

    accounts = []
    messages = []
    for i, ws in enumerate((ws_a, ws_b, ws_c)):
        account = SocialAccount.objects.create(
            workspace=ws,
            platform="facebook",
            account_platform_id=f"synthetic-page-{i}",
            account_name=f"Synthetic Page {i}",
            connection_status=SocialAccount.ConnectionStatus.CONNECTED,
        )
        message = InboxMessage.objects.create(
            workspace=ws,
            social_account=account,
            platform_message_id=f"synthetic-message-{i}",
            message_type=InboxMessage.MessageType.COMMENT,
            sender_name=f"Synthetic Sender {i}",
            body=f"synthetic-private-body-{i}",
            received_at=timezone.now(),
        )
        accounts.append(account)
        messages.append(message)

    key = services.issue_api_key(
        workspace=ws_a,
        social_accounts=[accounts[0]],
        issued_by=user,
        name="client-a-only",
        permissions=["use_inbox", "reply_from_inbox"],
    )
    rest = _SecureClient(HTTP_AUTHORIZATION=f"Bearer {key.plaintext_token}")
    web = _SecureClient()
    web.force_login(user)
    return SimpleNamespace(
        user=user,
        workspaces=(ws_a, ws_b, ws_c),
        accounts=accounts,
        messages=messages,
        rest=rest,
        web=web,
    )


def _call_mcp(client: Client, name: str, arguments: dict):
    return client.post(
        "/api/v1/mcp/",
        data=json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            }
        ),
        content_type="application/json",
    )


@pytest.mark.django_db
class TestThreeClientIsolation:
    def test_rest_list_sees_only_client_a(self, clients):
        context = clients
        response = context.rest.get("/api/v1/inbox/")
        assert response.status_code == 200, response.content
        visible_ids = {row["id"] for row in response.json()["messages"]}
        assert visible_ids == {str(context.messages[0].id)}
        assert "synthetic-private-body-1" not in response.content.decode()
        assert "synthetic-private-body-2" not in response.content.decode()

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_rest_read_denies_other_clients(self, clients, other_idx):
        context = clients
        response = context.rest.get(f"/api/v1/inbox/{context.messages[other_idx].id}")
        assert response.status_code == 404
        assert f"synthetic-private-body-{other_idx}" not in response.content.decode()

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_rest_cannot_create_reply_on_foreign_message(self, clients, other_idx):
        context = clients
        response = context.rest.post(
            f"/api/v1/inbox/{context.messages[other_idx].id}/replies",
            data=json.dumps({"body": "forbidden draft"}),
            content_type="application/json",
        )
        assert response.status_code == 404
        assert InboxReply.objects.count() == 0

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_rest_cannot_edit_or_discard_foreign_reply(self, clients, other_idx):
        context = clients
        foreign_reply = InboxReply.objects.create(
            inbox_message=context.messages[other_idx], body="confidential draft"
        )
        patch_response = context.rest.patch(
            f"/api/v1/inbox/replies/{foreign_reply.id}",
            data=json.dumps({"body": "unauthorized edit"}),
            content_type="application/json",
        )
        reply_url = f"/api/v1/inbox/replies/{foreign_reply.id}"
        delete_response = context.rest.delete(reply_url)
        assert patch_response.status_code == 404
        assert delete_response.status_code == 404
        foreign_reply.refresh_from_db()
        assert foreign_reply.body == "confidential draft"

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_rest_cannot_send_foreign_draft(self, clients, other_idx):
        context = clients
        reply = InboxReply.objects.create(
            inbox_message=context.messages[other_idx], body="do not send"
        )
        with patch("apps.inbox.services._dispatch_to_platform") as dispatch:
            response = context.rest.post(f"/api/v1/inbox/replies/{reply.id}/send")
        assert response.status_code == 404
        dispatch.assert_not_called()
        reply.refresh_from_db()
        assert reply.status == InboxReply.Status.DRAFT

    def test_mcp_list_sees_only_client_a(self, clients):
        context = clients
        response = _call_mcp(context.rest, "list_inbox_messages", {})
        data = response.json()
        assert "result" in data, data
        payload = json.loads(data["result"]["content"][0]["text"])
        visible_ids = {row["id"] for row in payload["messages"]}
        assert visible_ids == {str(context.messages[0].id)}
        assert "synthetic-private-body-1" not in response.content.decode()
        assert "synthetic-private-body-2" not in response.content.decode()

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_mcp_rejects_foreign_message_id(self, clients, other_idx):
        context = clients
        response = _call_mcp(
            context.rest,
            "get_inbox_message",
            {"message_id": str(context.messages[other_idx].id)},
        )
        data = response.json()
        assert "error" in data, data
        assert f"synthetic-private-body-{other_idx}" not in response.content.decode()

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_htmx_denies_other_client_workspaces(self, clients, other_idx):
        context = clients
        workspace = context.workspaces[other_idx]
        response = context.web.get(f"/workspace/{workspace.id}/inbox/")
        assert response.status_code == 403
        assert f"synthetic-private-body-{other_idx}" not in response.content.decode()

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_key_cannot_include_other_client_social_account(self, clients, other_idx):
        context = clients
        with pytest.raises(ValueError, match="does not belong to workspace"):
            services.issue_api_key(
                workspace=context.workspaces[0],
                social_accounts=[context.accounts[other_idx]],
                issued_by=context.user,
                name="invalid-cross-workspace",
                permissions=["use_inbox"],
            )
