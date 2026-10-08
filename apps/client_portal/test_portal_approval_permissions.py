"""Live portal approval permissions: deny stale sessions after a role change."""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.approvals.models import ApprovalAction
from apps.composer.models import PlatformPost, Post
from apps.members.models import CustomRole, WorkspaceMembership
from apps.organizations.models import Organization
from apps.social_accounts.models import SocialAccount
from apps.workspaces.models import Workspace


class PortalApprovalPermissionTests(TestCase):
    ACTIONS = (
        ("approve", "pending_client", "approved"),
        ("request_changes", "pending_client", "changes_requested"),
        ("reject", "pending_client", "rejected"),
        ("request_hold", "approved", "on_hold"),
    )

    def setUp(self):
        self.org_a = Organization.objects.create(name="Synthetic O1")
        self.org_c = Organization.objects.create(name="Synthetic O2")
        self.workspace_a = Workspace.objects.create(organization=self.org_a, name="Client A")
        self.workspace_b = Workspace.objects.create(organization=self.org_a, name="Client B")
        self.workspace_c = Workspace.objects.create(organization=self.org_c, name="Client C")
        self.user = User.objects.create_user(
            email="portal-a@example.invalid",
            password="synthetic-test-password",
            tos_accepted_at=timezone.now(),
        )
        self.membership = WorkspaceMembership.objects.create(
            user=self.user,
            workspace=self.workspace_a,
            workspace_role=WorkspaceMembership.WorkspaceRole.CLIENT,
        )
        self.sequence = 0
        self.client.force_login(self.user)
        session = self.client.session
        session["is_portal_session"] = True
        session["portal_workspace_id"] = str(self.workspace_a.id)
        session.save()

    def _make_post(self, workspace, status):
        self.sequence += 1
        account = SocialAccount.objects.create(
            workspace=workspace,
            platform="linkedin_personal",
            account_platform_id=f"synthetic-{self.sequence}",
            account_name=f"Synthetic account {self.sequence}",
            connection_status=SocialAccount.ConnectionStatus.CONNECTED,
        )
        post = Post.objects.create(
            workspace=workspace,
            author=self.user,
            caption=f"Synthetic post {self.sequence}",
        )
        platform_post = PlatformPost.objects.create(
            post=post,
            social_account=account,
            status=status,
        )
        return post, platform_post

    def _call(self, action, post):
        return self.client.post(
            reverse(f"client_portal:{action}", kwargs={"post_id": post.id}),
            {"comment": "Synthetic client feedback"},
        )

    def _assert_actions_denied(self):
        for action, original_status, _ in self.ACTIONS:
            with self.subTest(action=action):
                post, platform_post = self._make_post(self.workspace_a, original_status)
                response = self._call(action, post)
                self.assertEqual(response.status_code, 403)
                platform_post.refresh_from_db()
                self.assertEqual(platform_post.status, original_status)
                self.assertFalse(ApprovalAction.objects.filter(post=post).exists())

    def test_editor_and_viewer_with_existing_portal_session_cannot_act(self):
        for role in (
            WorkspaceMembership.WorkspaceRole.EDITOR,
            WorkspaceMembership.WorkspaceRole.VIEWER,
        ):
            with self.subTest(role=role):
                self.membership.workspace_role = role
                self.membership.save(update_fields=["workspace_role"])
                self._assert_actions_denied()

    def test_custom_role_without_approve_posts_cannot_act(self):
        custom = CustomRole.objects.create(
            organization=self.org_a,
            name="Synthetic no approval",
            permissions={"approve_posts": False, "view_analytics": True},
        )
        self.membership.custom_role = custom
        self.membership.save(update_fields=["custom_role"])
        self._assert_actions_denied()

    def test_client_can_still_perform_existing_portal_actions(self):
        for action, original_status, expected_status in self.ACTIONS:
            with self.subTest(action=action):
                post, platform_post = self._make_post(self.workspace_a, original_status)
                response = self._call(action, post)
                self.assertEqual(response.status_code, 302)
                platform_post.refresh_from_db()
                self.assertEqual(platform_post.status, expected_status)
                self.assertTrue(ApprovalAction.objects.filter(post=post).exists())

    def test_custom_role_with_explicit_approval_permission_can_act(self):
        custom = CustomRole.objects.create(
            organization=self.org_a,
            name="Synthetic approval allowed",
            permissions={"approve_posts": True},
        )
        self.membership.workspace_role = WorkspaceMembership.WorkspaceRole.EDITOR
        self.membership.custom_role = custom
        self.membership.save(update_fields=["workspace_role", "custom_role"])
        post, platform_post = self._make_post(self.workspace_a, "pending_client")
        response = self._call("approve", post)
        self.assertEqual(response.status_code, 302)
        platform_post.refresh_from_db()
        self.assertEqual(platform_post.status, "approved")

    def test_foreign_post_uuid_in_same_or_other_org_is_denied(self):
        for workspace in (self.workspace_b, self.workspace_c):
            with self.subTest(workspace=workspace.name):
                post, platform_post = self._make_post(workspace, "pending_client")
                response = self._call("approve", post)
                self.assertEqual(response.status_code, 404)
                platform_post.refresh_from_db()
                self.assertEqual(platform_post.status, "pending_client")
                self.assertFalse(ApprovalAction.objects.filter(post=post).exists())

    def test_removed_membership_cannot_act_with_existing_session(self):
        post, platform_post = self._make_post(self.workspace_a, "pending_client")
        self.membership.delete()
        response = self._call("approve", post)
        self.assertRedirects(response, reverse("client_portal:magic_link_expired"))
        platform_post.refresh_from_db()
        self.assertEqual(platform_post.status, "pending_client")
        self.assertFalse(ApprovalAction.objects.filter(post=post).exists())
