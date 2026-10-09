"""Synthetic cross-client OAuth/MCP and API-key revocation regressions.

The existing BrightBean membership resolution is exercised end-to-end.
These tests do not grant cross-tenant access and do not contact providers.
"""

from __future__ import annotations

import json

import pytest

from apps.api.tests.test_cross_client_isolation import (
    _call_mcp,
    _SecureClient,
)
from apps.api.tests.test_cross_client_isolation import (
    clients as clients,
)
from apps.composer.models import Post
from apps.mcp.tests.test_oauth_auth import _mint_oauth_token
from apps.members.models import WorkspaceMembership


@pytest.fixture
def oauth_for_a(clients):
    user = clients.user
    user.last_workspace_id = clients.workspaces[0].id
    user.save(update_fields=["last_workspace_id"])
    token = _mint_oauth_token(user)
    return _SecureClient(HTTP_AUTHORIZATION=f"Bearer {token}")


def _accounts(oauth):
    response = _call_mcp(oauth, "list_accounts", {})
    assert response.status_code == 200, response.content
    data = response.json()
    assert "result" in data, data
    return json.loads(data["result"]["content"][0]["text"])["accounts"]


def _grant_b_viewer(clients):
    return WorkspaceMembership.objects.create(
        user=clients.user,
        workspace=clients.workspaces[1],
        workspace_role=WorkspaceMembership.WorkspaceRole.VIEWER,
    )


@pytest.mark.django_db
class TestCrossClientOAuthBoundaries:
    def test_oauth_active_client_a_lists_only_a(self, clients, oauth_for_a):
        account_ids = {row["id"] for row in _accounts(oauth_for_a)}
        assert account_ids == {str(clients.accounts[0].id)}

    def test_oauth_switch_to_b_restricts_accounts_to_b(self, clients, oauth_for_a):
        _grant_b_viewer(clients)
        clients.user.last_workspace_id = clients.workspaces[1].id
        clients.user.save(update_fields=["last_workspace_id"])
        account_ids = {row["id"] for row in _accounts(oauth_for_a)}
        assert account_ids == {str(clients.accounts[1].id)}

    def test_oauth_viewer_b_cannot_create_draft(self, clients, oauth_for_a):
        _grant_b_viewer(clients)
        clients.user.last_workspace_id = clients.workspaces[1].id
        clients.user.save(update_fields=["last_workspace_id"])
        response = _call_mcp(
            oauth_for_a,
            "create_draft",
            {"social_account_id": str(clients.accounts[1].id), "caption": "forbidden"},
        )
        assert response.status_code == 200
        assert "error" in response.json()
        assert "Permission denied" in response.json()["error"]["message"]
        assert not Post.objects.filter(workspace=clients.workspaces[1]).exists()

    def test_oauth_viewer_b_cannot_read_inbox(self, clients, oauth_for_a):
        _grant_b_viewer(clients)
        clients.user.last_workspace_id = clients.workspaces[1].id
        clients.user.save(update_fields=["last_workspace_id"])
        response = _call_mcp(oauth_for_a, "list_inbox_messages", {})
        assert response.status_code == 200
        assert "error" in response.json()
        assert "Permission denied" in response.json()["error"]["message"]
        assert "synthetic-private-body-1" not in response.content.decode()

    @pytest.mark.parametrize("other_idx", [1, 2])
    def test_oauth_a_cannot_get_other_client_message(self, clients, oauth_for_a, other_idx):
        response = _call_mcp(
            oauth_for_a,
            "get_inbox_message",
            {"message_id": str(clients.messages[other_idx].id)},
        )
        assert response.status_code == 200
        assert "error" in response.json()
        assert f"synthetic-private-body-{other_idx}" not in response.content.decode()

    def test_oauth_stale_last_workspace_c_does_not_grant_c(self, clients, oauth_for_a):
        clients.user.last_workspace_id = clients.workspaces[2].id
        clients.user.save(update_fields=["last_workspace_id"])
        account_ids = {row["id"] for row in _accounts(oauth_for_a)}
        assert str(clients.accounts[2].id) not in account_ids

    def test_oauth_all_memberships_revoked_returns_401(self, clients, oauth_for_a):
        WorkspaceMembership.objects.filter(user=clients.user).delete()
        response = _call_mcp(oauth_for_a, "list_accounts", {})
        assert response.status_code == 401

    def test_api_key_issuer_offboarded_denied_in_rest_and_mcp(self, clients):
        WorkspaceMembership.objects.filter(user=clients.user, workspace=clients.workspaces[0]).delete()
        rest = clients.rest.get("/api/v1/accounts/")
        mcp = _call_mcp(clients.rest, "list_accounts", {})
        assert rest.status_code == 401
        assert mcp.status_code == 401

    def test_api_key_issuer_demoted_cannot_read_inbox(self, clients):
        membership = WorkspaceMembership.objects.get(user=clients.user, workspace=clients.workspaces[0])
        membership.workspace_role = WorkspaceMembership.WorkspaceRole.VIEWER
        membership.save(update_fields=["workspace_role"])
        response = clients.rest.get("/api/v1/inbox/")
        assert response.status_code == 403
        assert "synthetic-private-body-0" not in response.content.decode()


@pytest.mark.django_db
class TestCachedKeyAuthorizationBoundaries:
    """A previously used bearer must not preserve stale permissions."""

    def test_cached_key_revoked_denies_rest_and_mcp(self, clients):
        from apps.api_keys import services
        from apps.api_keys.models import ApiKey

        assert clients.rest.get("/api/v1/accounts/").status_code == 200
        key = ApiKey.objects.get(name="client-a-only")
        services.revoke_api_key(key)
        assert clients.rest.get("/api/v1/accounts/").status_code == 401
        assert _call_mcp(clients.rest, "list_accounts", {}).status_code == 401

    def test_cached_key_permissions_reduced_denies_inbox(self, clients):
        from apps.api_keys.models import ApiKey

        assert clients.rest.get("/api/v1/inbox/").status_code == 200
        key = ApiKey.objects.get(name="client-a-only")
        key.permissions = []
        key.save(update_fields=["permissions"])
        assert clients.rest.get("/api/v1/inbox/").status_code == 403
        response = _call_mcp(clients.rest, "list_inbox_messages", {})
        assert response.status_code == 200
        assert "error" in response.json()
        assert "synthetic-private-body-0" not in response.content.decode()

    def test_cached_key_forward_allowlist_remove(self, clients):
        from apps.api_keys.models import ApiKey

        assert len(_accounts(clients.rest)) == 1
        key = ApiKey.objects.get(name="client-a-only")
        key.social_accounts.remove(clients.accounts[0])
        response = clients.rest.get("/api/v1/accounts/")
        assert response.status_code == 200
        assert response.json()["accounts"] == []
        assert _accounts(clients.rest) == []

    def test_cached_key_reverse_allowlist_remove(self, clients):
        from apps.api_keys.models import ApiKey

        assert len(_accounts(clients.rest)) == 1
        key = ApiKey.objects.get(name="client-a-only")
        clients.accounts[0].api_keys.remove(key)
        assert _accounts(clients.rest) == []

    def test_cached_key_reverse_allowlist_clear(self, clients):
        assert len(_accounts(clients.rest)) == 1
        clients.accounts[0].api_keys.clear()
        assert _accounts(clients.rest) == []

    def test_cached_key_offboarding_denies_rest_and_mcp(self, clients):
        assert clients.rest.get("/api/v1/accounts/").status_code == 200
        WorkspaceMembership.objects.filter(user=clients.user, workspace=clients.workspaces[0]).delete()
        assert clients.rest.get("/api/v1/accounts/").status_code == 401
        assert _call_mcp(clients.rest, "list_accounts", {}).status_code == 401

    def test_cached_key_expiry_change_denies_next_request(self, clients):
        from datetime import timedelta

        from django.utils import timezone

        from apps.api_keys.models import ApiKey

        assert clients.rest.get("/api/v1/accounts/").status_code == 200
        key = ApiKey.objects.get(name="client-a-only")
        key.expires_at = timezone.now() - timedelta(seconds=1)
        key.save(update_fields=["expires_at"])
        assert clients.rest.get("/api/v1/accounts/").status_code == 401
