"""Magic links must not authenticate clients after membership or account revocation."""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.client_portal.models import MagicLinkToken
from apps.client_portal.services import consume_magic_link, peek_magic_link
from apps.members.models import WorkspaceMembership
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace


class RevokedMagicLinkTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Synthetic Clients")
        self.workspace = Workspace.objects.create(organization=self.organization, name="Client A")
        self.user = User.objects.create_user(
            email="revoked-client@example.test",
            password="test-pass",
            tos_accepted_at=timezone.now(),
        )
        self.membership = WorkspaceMembership.objects.create(
            user=self.user,
            workspace=self.workspace,
            workspace_role=WorkspaceMembership.WorkspaceRole.CLIENT,
        )
        self.token = MagicLinkToken.objects.create(user=self.user, workspace=self.workspace)

    def _assert_denied(self):
        self.assertIsNone(peek_magic_link(self.token.token))
        self.assertEqual(consume_magic_link(self.token.token), (None, None, False))
        self.token.refresh_from_db()
        self.assertFalse(self.token.is_consumed)

    def test_removed_membership_rejects_existing_link(self):
        self.membership.delete()
        self._assert_denied()

    def test_role_changed_to_editor_rejects_old_client_link(self):
        self.membership.workspace_role = WorkspaceMembership.WorkspaceRole.EDITOR
        self.membership.save(update_fields=["workspace_role"])
        self._assert_denied()

    def test_deactivated_user_rejects_existing_link(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        self._assert_denied()

    def test_archived_workspace_rejects_existing_link(self):
        self.workspace.is_archived = True
        self.workspace.save(update_fields=["is_archived"])
        self._assert_denied()

    def test_removed_and_readmitted_client_cannot_reuse_old_link(self):
        self.membership.delete()
        WorkspaceMembership.objects.create(
            user=self.user,
            workspace=self.workspace,
            workspace_role=WorkspaceMembership.WorkspaceRole.CLIENT,
        )
        self._assert_denied()

    def test_revoked_link_post_does_not_authenticate_user(self):
        self.membership.delete()
        response = self.client.post(
            reverse("client_portal:magic_link_entry", kwargs={"token": self.token.token})
        )
        self.assertRedirects(response, reverse("client_portal:magic_link_expired"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertNotIn("is_portal_session", self.client.session)

    def test_new_link_for_current_client_still_works(self):
        user, workspace, valid = consume_magic_link(self.token.token)
        self.assertTrue(valid)
        self.assertEqual(user, self.user)
        self.assertEqual(workspace, self.workspace)
