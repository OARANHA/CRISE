"""Security regression tests for approvals comments (V9)."""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.approvals.comments import delete_comment as delete_comment_service
from apps.approvals.models import PostComment
from apps.composer.models import Post
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace


def _make_user(email):
    user = User.objects.create_user(
        email=email,
        password="testpass123",
        tos_accepted_at=timezone.now(),
    )
    # The accounts post_save signal auto-provisions a default Organization +
    # Workspace + OrgMembership for every new User. Tests that want to attach
    # the user to a specific org must start from a clean slate, otherwise the
    # RBAC middleware (which does OrgMembership.objects.filter(...).first())
    # may pick the auto-org instead of the test org.
    from apps.members.models import OrgMembership, WorkspaceMembership
    from apps.organizations.models import Organization

    auto_org_ids = list(OrgMembership.objects.filter(user=user).values_list("organization_id", flat=True))
    WorkspaceMembership.objects.filter(user=user).delete()
    OrgMembership.objects.filter(user=user).delete()
    Organization.objects.filter(id__in=auto_org_ids).delete()
    return user


class EditCommentWorkspaceScopeTests(TestCase):
    """V9: edit_comment must reject cross-workspace post_id."""

    def setUp(self):
        self.org = Organization.objects.create(name="Test Org")
        self.ws_a = Workspace.objects.create(organization=self.org, name="WS-A")
        self.ws_b = Workspace.objects.create(organization=self.org, name="WS-B")
        self.user = _make_user("user@example.com")
        OrgMembership.objects.create(user=self.user, organization=self.org, org_role="owner")
        WorkspaceMembership.objects.create(user=self.user, workspace=self.ws_a, workspace_role="editor")
        WorkspaceMembership.objects.create(user=self.user, workspace=self.ws_b, workspace_role="editor")

        self.post_b = Post.objects.create(workspace=self.ws_b, author=self.user, caption="b")
        self.comment = PostComment.objects.create(
            post=self.post_b,
            author=self.user,
            body="hi",
            visibility=PostComment.Visibility.INTERNAL,
        )

    def test_cross_workspace_edit_returns_404(self):
        self.client.force_login(self.user)
        # Edit a comment that lives in WS-B, but POST through WS-A's URL.
        url = reverse(
            "approvals:edit_comment",
            kwargs={
                "workspace_id": self.ws_a.id,
                "post_id": self.post_b.id,
                "comment_id": self.comment.id,
            },
        )
        response = self.client.post(url, data={"body": "rewritten"})
        self.assertEqual(response.status_code, 404)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, "hi")

    def test_same_workspace_edit_succeeds(self):
        self.client.force_login(self.user)
        url = reverse(
            "approvals:edit_comment",
            kwargs={
                "workspace_id": self.ws_b.id,
                "post_id": self.post_b.id,
                "comment_id": self.comment.id,
            },
        )
        response = self.client.post(url, data={"body": "rewritten"})
        self.assertLess(response.status_code, 400)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, "rewritten")


class DeleteCommentWorkspaceBoundaryTests(EditCommentWorkspaceScopeTests):
    """Negative IDOR cases, plus preserving intended same-workspace deletion."""

    def _delete_url(self, workspace, post, comment):
        return reverse(
            "approvals:delete_comment",
            kwargs={
                "workspace_id": workspace.id,
                "post_id": post.id,
                "comment_id": comment.id,
            },
        )

    def _manager(self, email, workspace):
        manager = _make_user(email)
        OrgMembership.objects.create(user=manager, organization=workspace.organization, org_role="member")
        WorkspaceMembership.objects.create(user=manager, workspace=workspace, workspace_role="manager")
        return manager

    def test_author_cannot_delete_other_workspace_comment_using_foreign_url(self):
        self.client.force_login(self.user)
        response = self.client.post(self._delete_url(self.ws_a, self.post_b, self.comment))
        self.assertEqual(response.status_code, 404)
        self.comment.refresh_from_db()
        self.assertIsNone(self.comment.deleted_at)

    def test_wrong_post_uuid_in_same_workspace_cannot_delete_comment(self):
        unrelated_post = Post.objects.create(workspace=self.ws_b, author=self.user, caption="other")
        self.client.force_login(self.user)
        response = self.client.post(self._delete_url(self.ws_b, unrelated_post, self.comment))
        self.assertEqual(response.status_code, 404)
        self.comment.refresh_from_db()
        self.assertIsNone(self.comment.deleted_at)

    def test_manager_from_a_cannot_delete_b_comment_via_service(self):
        manager_a = self._manager("manager-a@example.test", self.ws_a)
        with self.assertRaisesRegex(ValueError, "Comment not found"):
            delete_comment_service(self.comment.id, manager_a, self.ws_a)
        self.comment.refresh_from_db()
        self.assertIsNone(self.comment.deleted_at)

    def test_author_can_delete_comment_in_own_workspace(self):
        self.client.force_login(self.user)
        response = self.client.post(self._delete_url(self.ws_b, self.post_b, self.comment))
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertIsNotNone(self.comment.deleted_at)

    def test_manager_can_moderate_comment_in_own_workspace(self):
        manager_b = self._manager("manager-b@example.test", self.ws_b)
        self.client.force_login(manager_b)
        response = self.client.post(self._delete_url(self.ws_b, self.post_b, self.comment))
        self.assertEqual(response.status_code, 200)
        self.comment.refresh_from_db()
        self.assertIsNotNone(self.comment.deleted_at)

    def test_non_author_contributor_cannot_delete_same_workspace_comment(self):
        contributor = _make_user("contributor-b@example.test")
        OrgMembership.objects.create(user=contributor, organization=self.org, org_role="member")
        WorkspaceMembership.objects.create(user=contributor, workspace=self.ws_b, workspace_role="contributor")
        self.client.force_login(contributor)
        response = self.client.post(self._delete_url(self.ws_b, self.post_b, self.comment))
        self.assertEqual(response.status_code, 403)
        self.comment.refresh_from_db()
        self.assertIsNone(self.comment.deleted_at)

    def test_manager_a_cannot_delete_comment_in_other_organization_via_service(self):
        org_c = Organization.objects.create(name="Other org")
        ws_c = Workspace.objects.create(organization=org_c, name="Client C")
        post_c = Post.objects.create(workspace=ws_c, author=self.user, caption="C")
        comment_c = PostComment.objects.create(post=post_c, author=self.user, body="private c")
        manager_a = self._manager("manager-a-for-c@example.test", self.ws_a)
        with self.assertRaisesRegex(ValueError, "Comment not found"):
            delete_comment_service(comment_c.id, manager_a, self.ws_a)
        comment_c.refresh_from_db()
        self.assertIsNone(comment_c.deleted_at)
