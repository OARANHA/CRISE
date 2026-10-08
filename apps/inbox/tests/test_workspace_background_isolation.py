"""Synthetic A/B/C workspace isolation for background inbox synchronization.

Uses the existing BrightBean sync engine without provider/network calls.
Tests the account-owned database rows and notification recipient scope.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.utils import timezone

from apps.accounts.models import User
from apps.api.tests.test_cross_client_isolation import clients as clients
from apps.inbox.models import InboxMessage
from apps.inbox.tasks import InboxSyncEngine
from apps.members.models import OrgMembership, WorkspaceMembership


def _incoming(message_id: str, body: str):
    return SimpleNamespace(
        platform_message_id=message_id,
        sender_name="Synthetic Sender",
        sender_id="synthetic-sender",
        text=body,
        message_type=InboxMessage.MessageType.DM,
        timestamp=timezone.now(),
        extra={},
    )


@pytest.mark.django_db
class TestBackgroundInboxWorkspaceIsolation:
    def test_sync_cycle_considers_all_three_accounts_without_providers(self, clients):
        engine = InboxSyncEngine()
        with patch.object(engine, "_sync_account") as sync_account:
            engine.sync_all()
        seen = {call.args[0].id for call in sync_account.call_args_list}
        assert seen == {account.id for account in clients.accounts}

    def test_same_remote_message_id_stays_distinct_per_account(self, clients):
        engine = InboxSyncEngine()
        for index, account in enumerate(clients.accounts):
            engine._upsert_message(account, _incoming("same-remote-id", f"client-{index}"), notify=False)
        rows = InboxMessage.objects.filter(platform_message_id="same-remote-id")
        assert rows.count() == 3
        data = {row.workspace_id: row.body for row in rows}
        assert data == {clients.workspaces[i].id: f"client-{i}" for i in range(3)}

    def test_updating_client_a_does_not_mutate_b_or_c(self, clients):
        engine = InboxSyncEngine()
        for index, account in enumerate(clients.accounts):
            engine._upsert_message(account, _incoming("same-event", f"original-{index}"), notify=False)
        engine._upsert_message(clients.accounts[0], _incoming("same-event", "updated-a"), notify=False)
        rows = InboxMessage.objects.filter(platform_message_id="same-event")
        assert rows.count() == 3
        data = {row.workspace_id: row.body for row in rows}
        assert data[clients.workspaces[0].id] == "updated-a"
        assert data[clients.workspaces[1].id] == "original-1"
        assert data[clients.workspaces[2].id] == "original-2"

    def test_new_message_notifies_only_its_workspace_members(self, clients):
        user_b = User.objects.create_user(
            email="synthetic-owner-b@example.test",
            password="synthetic-test-password",
            name="Synthetic Owner B",
            tos_accepted_at=timezone.now(),
        )
        OrgMembership.objects.create(
            user=user_b,
            organization=clients.workspaces[1].organization,
            org_role=OrgMembership.OrgRole.MEMBER,
        )
        WorkspaceMembership.objects.create(
            user=user_b,
            workspace=clients.workspaces[1],
            workspace_role=WorkspaceMembership.WorkspaceRole.OWNER,
        )
        with patch("apps.inbox.tasks.notify") as send:
            InboxSyncEngine()._upsert_message(
                clients.accounts[1], _incoming("notify-only-b", "private-b"), notify=True
            )
        send.assert_called_once()
        assert send.call_args.kwargs["user"] == user_b
        assert send.call_args.kwargs["data"]["workspace_id"] == str(clients.workspaces[1].id)

    def test_existing_message_update_does_not_renotify_client(self, clients):
        engine = InboxSyncEngine()
        with patch("apps.inbox.tasks.notify") as send:
            engine._upsert_message(clients.accounts[0], _incoming("updated-once", "first"), notify=True)
            engine._upsert_message(clients.accounts[0], _incoming("updated-once", "second"), notify=True)
        send.assert_called_once()
        message = InboxMessage.objects.get(
            social_account=clients.accounts[0], platform_message_id="updated-once"
        )
        assert message.workspace_id == clients.workspaces[0].id
        assert message.body == "second"
