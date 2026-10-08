"""Client comment replies use the same visibility rules as top-level comments.

Synthetic workspaces only; no social provider requests or real client content.
"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.approvals.comments import get_comments_for_post
from apps.approvals.models import PostComment
from apps.composer.models import Post
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace


def _member(organization, workspace, *, email, role):
    user = User.objects.create_user(
        email=email,
        password="synthetic-test-password",
        tos_accepted_at=timezone.now(),
    )
    # The original signal provisions a default org/workspace per new user.
    auto_org_ids = list(OrgMembership.objects.filter(user=user).values_list("organization_id", flat=True))
    WorkspaceMembership.objects.filter(user=user).delete()
    OrgMembership.objects.filter(user=user).delete()
    Organization.objects.filter(id__in=auto_org_ids).delete()
    OrgMembership.objects.create(user=user, organization=organization, org_role="member")
    WorkspaceMembership.objects.create(user=user, workspace=workspace, workspace_role=role)
    return user


class ClientCommentReplyVisibilityTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Synthetic Organization")
        self.workspace = Workspace.objects.create(organization=self.organization, name="Synthetic Client")
        self.editor = _member(
            self.organization,
            self.workspace,
            email="editor-replies@example.test",
            role=WorkspaceMembership.WorkspaceRole.EDITOR,
        )
        self.client_user = _member(
            self.organization,
            self.workspace,
            email="client-replies@example.test",
            role=WorkspaceMembership.WorkspaceRole.CLIENT,
        )
        self.post = Post.objects.create(workspace=self.workspace, author=self.editor, caption="Synthetic post")
        self.external = PostComment.objects.create(
            post=self.post,
            author=self.editor,
            body="visible-external-root",
            visibility=PostComment.Visibility.EXTERNAL,
        )
        PostComment.objects.create(
            post=self.post,
            author=self.editor,
            body="hidden-internal-root",
            visibility=PostComment.Visibility.INTERNAL,
        )
        PostComment.objects.create(
            post=self.post,
            author=self.editor,
            parent_comment=self.external,
            body="visible-external-reply",
            visibility=PostComment.Visibility.EXTERNAL,
        )
        PostComment.objects.create(
            post=self.post,
            author=self.editor,
            parent_comment=self.external,
            body="hidden-internal-reply",
            visibility=PostComment.Visibility.INTERNAL,
        )

    def _visible(self, user):
        return {
            root.body: [reply.body for reply in root.replies.all()] for root in get_comments_for_post(self.post, user)
        }

    def test_client_sees_only_external_root_and_external_reply(self):
        self.assertEqual(
            self._visible(self.client_user),
            {"visible-external-root": ["visible-external-reply"]},
        )

    def test_editor_keeps_access_to_team_comment_and_reply(self):
        result = self._visible(self.editor)
        self.assertEqual(result["visible-external-root"], ["visible-external-reply", "hidden-internal-reply"])
        self.assertEqual(result["hidden-internal-root"], [])

    def test_downgrade_editor_to_client_filters_existing_replies(self):
        membership = WorkspaceMembership.objects.get(user=self.editor, workspace=self.workspace)
        membership.workspace_role = WorkspaceMembership.WorkspaceRole.CLIENT
        membership.save(update_fields=["workspace_role"])
        self.assertEqual(
            self._visible(self.editor),
            {"visible-external-root": ["visible-external-reply"]},
        )

    def test_client_comment_response_does_not_render_internal_reply(self):
        self.client.force_login(self.client_user)
        url = reverse(
            "approvals:add_comment",
            kwargs={"workspace_id": self.workspace.id, "post_id": self.post.id},
        )
        response = self.client.post(url, {"body": "new-external-comment", "visibility": "external"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "visible-external-reply")
        self.assertContains(response, "new-external-comment")
        self.assertNotContains(response, "hidden-internal-reply")
        self.assertNotContains(response, "hidden-internal-root")
