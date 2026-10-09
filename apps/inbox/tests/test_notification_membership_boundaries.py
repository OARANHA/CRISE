"""Guard private inbox notifications against stale or cross-client assignees.

The normal assignment UI already checks membership; these synthetic tests
cover database state that becomes stale after an employee loses access.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from django.utils import timezone

from apps.accounts.models import User
from apps.api.tests.test_cross_client_isolation import clients as clients
from apps.inbox.models import InboxSLAConfig
from apps.inbox.tasks import InboxSyncEngine
from apps.members.models import OrgMembership, WorkspaceMembership


def _notify(engine, message, kind):
    if kind == "new":
        engine._notify_new_message(message)
    else:
        config = InboxSLAConfig(workspace=message.workspace, target_response_minutes=120)
        engine._notify_sla_overdue(message, config)


def _foreign_member(clients, index):
    workspace = clients.workspaces[index]
    user = User.objects.create_user(
        email=f"foreign-assignee-{index}@example.test",
        password="synthetic-test-password",
        name="Synthetic Foreign Assignee",
        tos_accepted_at=timezone.now(),
    )
    OrgMembership.objects.create(
        user=user,
        organization=workspace.organization,
        org_role=OrgMembership.OrgRole.MEMBER,
    )
    WorkspaceMembership.objects.create(
        user=user,
        workspace=workspace,
        workspace_role=WorkspaceMembership.WorkspaceRole.OWNER,
    )
    return user


@pytest.mark.django_db
class TestInboxNotificationMembershipBoundary:
    @pytest.mark.parametrize("kind", ["new", "sla"])
    def test_current_assignee_receives_notification(self, clients, kind):
        message = clients.messages[0]
        message.assigned_to = clients.user
        message.save(update_fields=["assigned_to"])

        with patch("apps.inbox.tasks.notify") as sender:
            _notify(InboxSyncEngine(), message, kind)

        sender.assert_called_once()
        assert sender.call_args.kwargs["user"] == clients.user
        assert sender.call_args.kwargs["data"]["workspace_id"] == str(clients.workspaces[0].id)

    @pytest.mark.parametrize("kind", ["new", "sla"])
    @pytest.mark.parametrize("foreign_idx", [1, 2])
    def test_foreign_assignee_is_not_notified(self, clients, kind, foreign_idx):
        foreign_user = _foreign_member(clients, foreign_idx)
        message = clients.messages[0]
        message.assigned_to = foreign_user
        message.save(update_fields=["assigned_to"])

        with patch("apps.inbox.tasks.notify") as sender:
            _notify(InboxSyncEngine(), message, kind)

        sender.assert_called_once()
        assert sender.call_args.kwargs["user"] == clients.user
        assert sender.call_args.kwargs["user"] != foreign_user
        assert sender.call_args.kwargs["data"]["workspace_id"] == str(clients.workspaces[0].id)

    @pytest.mark.parametrize("kind", ["new", "sla"])
    def test_offboarded_assignee_is_not_notified(self, clients, kind):
        message = clients.messages[0]
        message.assigned_to = clients.user
        message.save(update_fields=["assigned_to"])
        WorkspaceMembership.objects.filter(
            user=clients.user,
            workspace=clients.workspaces[0],
        ).delete()

        with patch("apps.inbox.tasks.notify") as sender:
            _notify(InboxSyncEngine(), message, kind)

        sender.assert_not_called()
