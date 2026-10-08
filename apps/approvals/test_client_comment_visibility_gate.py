"""HTTP regressions for forged internal comments by a CLIENT workspace member.

All identities and content are synthetic; no external providers or real clients.
"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.approvals.models import PostComment
from apps.composer.models import Post
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace


def _member(org, workspace, email, role):
    user = User.objects.create_user(
        email=email,
        password="synthetic-test-password",
        tos_accepted_at=timezone.now(),
    )
    # The upstream signal creates an unrelated default org per user.
    auto_org_ids = list(OrgMembership.objects.filter(user=user).values_list("organization_id", flat=True))
    WorkspaceMembership.objects.filter(user=user).delete()
    OrgMembership.objects.filter(user=user).delete()
    Organization.objects.filter(id__in=auto_org_ids).delete()

    OrgMembership.objects.create(user=user, organization=org, org_role=OrgMembership.OrgRole.MEMBER)
    WorkspaceMembership.objects.create(user=user, workspace=workspace, workspace_role=role)
    return user


class ClientCommentVisibilityGateTests(TestCase):
    def setUp(self):
        self.org_a = Organization.objects.create(name="Synthetic Org A")
        self.org_c = Organization.objects.create(name="Synthetic Org C")
        self.ws_a = Workspace.objects.create(organization=self.org_a, name="Client A")
        self.ws_b = Workspace.objects.create(organization=self.org_a, name="Client B")
        self.ws_c = Workspace.objects.create(organization=self.org_c, name="Client C")

        self.editor = _member(
            self.org_a,
            self.ws_a,
            "editor-a@example.test",
            WorkspaceMembership.WorkspaceRole.EDITOR,
        )
        self.client_a = _member(
            self.org_a,
            self.ws_a,
            "client-a@example.test",
            WorkspaceMembership.WorkspaceRole.CLIENT,
        )
        self.editor_b = _member(
            self.org_a,
            self.ws_b,
            "editor-b@example.test",
            WorkspaceMembership.WorkspaceRole.EDITOR,
        )
        self.editor_c = _member(
            self.org_c,
            self.ws_c,
            "editor-c@example.test",
            WorkspaceMembership.WorkspaceRole.EDITOR,
        )

        self.post_a = Post.objects.create(workspace=self.ws_a, author=self.editor, caption="Synthetic post A")
        self.post_b = Post.objects.create(workspace=self.ws_b, author=self.editor_b, caption="Synthetic post B")
        self.post_c = Post.objects.create(workspace=self.ws_c, author=self.editor_c, caption="Synthetic post C")

    @staticmethod
    def _url(workspace, post):
        return reverse(
            "approvals:add_comment",
            kwargs={"workspace_id": workspace.id, "post_id": post.id},
        )

    def test_client_cannot_forge_internal_comment_on_own_post(self):
        self.client.force_login(self.client_a)
        response = self.client.post(
            self._url(self.ws_a, self.post_a),
            {"body": "forged internal note", "visibility": PostComment.Visibility.INTERNAL},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(PostComment.objects.filter(post=self.post_a, body="forged internal note").exists())

    def test_client_cannot_use_unknown_visibility_to_bypass_gate(self):
        self.client.force_login(self.client_a)
        response = self.client.post(
            self._url(self.ws_a, self.post_a),
            {"body": "invalid scope", "visibility": "unexpected"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(PostComment.objects.filter(post=self.post_a).exists())

    def test_client_can_still_comment_externally(self):
        self.client.force_login(self.client_a)
        response = self.client.post(
            self._url(self.ws_a, self.post_a),
            {"body": "external reply", "visibility": PostComment.Visibility.EXTERNAL},
        )
        self.assertEqual(response.status_code, 200)
        comment = PostComment.objects.get(post=self.post_a, body="external reply")
        self.assertEqual(comment.visibility, PostComment.Visibility.EXTERNAL)

    def test_client_default_visibility_remains_external(self):
        self.client.force_login(self.client_a)
        response = self.client.post(self._url(self.ws_a, self.post_a), {"body": "default external"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            PostComment.objects.get(post=self.post_a).visibility,
            PostComment.Visibility.EXTERNAL,
        )

    def test_editor_keeps_internal_comments(self):
        self.client.force_login(self.editor)
        response = self.client.post(
            self._url(self.ws_a, self.post_a),
            {"body": "legitimate team note", "visibility": PostComment.Visibility.INTERNAL},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            PostComment.objects.get(post=self.post_a).visibility,
            PostComment.Visibility.INTERNAL,
        )

    def test_existing_session_uses_downgraded_role(self):
        self.client.force_login(self.editor)
        membership = WorkspaceMembership.objects.get(user=self.editor, workspace=self.ws_a)
        membership.workspace_role = WorkspaceMembership.WorkspaceRole.CLIENT
        membership.save(update_fields=["workspace_role"])

        response = self.client.post(
            self._url(self.ws_a, self.post_a),
            {"body": "after downgrade", "visibility": PostComment.Visibility.INTERNAL},
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(PostComment.objects.filter(post=self.post_a).exists())

    def test_client_cannot_comment_on_other_workspace_in_same_org(self):
        self.client.force_login(self.client_a)
        response = self.client.post(
            self._url(self.ws_b, self.post_b),
            {"body": "cross-workspace", "visibility": PostComment.Visibility.EXTERNAL},
        )
        self.assertIn(response.status_code, (403, 404))
        self.assertFalse(PostComment.objects.filter(post=self.post_b).exists())

    def test_client_cannot_comment_on_other_organization(self):
        self.client.force_login(self.client_a)
        response = self.client.post(
            self._url(self.ws_c, self.post_c),
            {"body": "cross-organization", "visibility": PostComment.Visibility.EXTERNAL},
        )
        self.assertIn(response.status_code, (403, 404))
        self.assertFalse(PostComment.objects.filter(post=self.post_c).exists())
