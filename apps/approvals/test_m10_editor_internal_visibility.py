"""M10 characterizations: EDITOR visibility is role-based, not actor-origin-based.

These tests intentionally demonstrate the existing BrightBean behavior, including
a VIGIAFAST policy gap. Passing tests do NOT mean external editors are safe to
receive internal comments. Only synthetic users, workspaces, and attachments.
"""

import shutil
import tempfile

from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.approvals.comments import get_comments_for_post
from apps.approvals.models import PostComment
from apps.composer.models import Post
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace

TEMP_MEDIA_ROOT = tempfile.mkdtemp(prefix="vigiafast-m10-")


def tearDownModule():
    shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


def _user_in_workspace(org, workspace, *, email, role):
    user = User.objects.create_user(
        email=email,
        password="synthetic-test-password",
        tos_accepted_at=timezone.now(),
    )
    # Existing account signal automatically provisions an unrelated organization.
    auto_org_ids = list(OrgMembership.objects.filter(user=user).values_list("organization_id", flat=True))
    WorkspaceMembership.objects.filter(user=user).delete()
    OrgMembership.objects.filter(user=user).delete()
    Organization.objects.filter(id__in=auto_org_ids).delete()
    OrgMembership.objects.create(user=user, organization=org, org_role=OrgMembership.OrgRole.MEMBER)
    WorkspaceMembership.objects.create(user=user, workspace=workspace, workspace_role=role)
    return user


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class M10EditorInternalVisibilityCharacterizationTests(TestCase):
    """Characterize, but do not endorse, built-in EDITOR access."""

    def setUp(self):
        self.org_o1 = Organization.objects.create(name="Synthetic O1")
        self.org_o2 = Organization.objects.create(name="Synthetic O2")
        self.ws_a = Workspace.objects.create(organization=self.org_o1, name="Synthetic A")
        self.ws_b = Workspace.objects.create(organization=self.org_o1, name="Synthetic B")
        self.ws_c = Workspace.objects.create(organization=self.org_o2, name="Synthetic C")

        # The labels I_A / E_A express the intended business affiliation only:
        # BOTH persist with precisely the same WorkspaceRole.EDITOR.
        self.internal_editor = _user_in_workspace(
            self.org_o1,
            self.ws_a,
            email="m10-internal-editor@example.test",
            role=WorkspaceMembership.WorkspaceRole.EDITOR,
        )
        self.external_editor = _user_in_workspace(
            self.org_o1,
            self.ws_a,
            email="m10-client-operator@example.test",
            role=WorkspaceMembership.WorkspaceRole.EDITOR,
        )
        self.observer = _user_in_workspace(
            self.org_o1,
            self.ws_a,
            email="m10-client-observer@example.test",
            role=WorkspaceMembership.WorkspaceRole.CLIENT,
        )
        self.post_a = Post.objects.create(workspace=self.ws_a, author=self.internal_editor, caption="A")
        self.post_b = Post.objects.create(workspace=self.ws_b, author=self.internal_editor, caption="B")
        self.post_c = Post.objects.create(workspace=self.ws_c, author=self.internal_editor, caption="C")

        self.internal_root = PostComment.objects.create(
            post=self.post_a,
            author=self.internal_editor,
            body="m10-internal-root",
            visibility=PostComment.Visibility.INTERNAL,
            attachment=ContentFile(b"private-root-a", name="m10-root-a.png"),
        )
        self.external_root = PostComment.objects.create(
            post=self.post_a,
            author=self.internal_editor,
            body="m10-external-root",
            visibility=PostComment.Visibility.EXTERNAL,
            attachment=ContentFile(b"public-comment-a", name="m10-external-a.png"),
        )
        self.internal_reply = PostComment.objects.create(
            post=self.post_a,
            author=self.internal_editor,
            parent_comment=self.external_root,
            body="m10-internal-reply",
            visibility=PostComment.Visibility.INTERNAL,
            attachment=ContentFile(b"private-reply-a", name="m10-reply-a.png"),
        )
        PostComment.objects.create(
            post=self.post_a,
            author=self.internal_editor,
            parent_comment=self.external_root,
            body="m10-external-reply",
            visibility=PostComment.Visibility.EXTERNAL,
        )
        self.comment_b = PostComment.objects.create(
            post=self.post_b,
            author=self.internal_editor,
            body="m10-internal-b",
            visibility=PostComment.Visibility.INTERNAL,
            attachment=ContentFile(b"private-b", name="m10-b.png"),
        )
        self.comment_c = PostComment.objects.create(
            post=self.post_c,
            author=self.internal_editor,
            body="m10-internal-c",
            visibility=PostComment.Visibility.INTERNAL,
            attachment=ContentFile(b"private-c", name="m10-c.png"),
        )

    def _visible(self, actor):
        return {
            root.body: [reply.body for reply in root.replies.all()]
            for root in get_comments_for_post(self.post_a, actor)
        }

    @staticmethod
    def _attachment_url(workspace, post, comment):
        return reverse(
            "approvals:comment_attachment",
            kwargs={
                "workspace_id": workspace.id,
                "post_id": post.id,
                "comment_id": comment.id,
            },
        )

    def _comments_url(self):
        return reverse(
            "approvals:add_comment",
            kwargs={"workspace_id": self.ws_a.id, "post_id": self.post_a.id},
        )

    def test_external_editor_and_internal_editor_have_same_visibility_today(self):
        for actor in (self.internal_editor, self.external_editor):
            with self.subTest(actor=actor.email):
                visible = self._visible(actor)
                self.assertIn("m10-internal-root", visible)
                self.assertIn("m10-internal-reply", visible["m10-external-root"])
                self.assertIn("m10-external-reply", visible["m10-external-root"])

    def test_external_editor_sees_internal_root_and_reply_in_htmx_response(self):
        self.client.force_login(self.external_editor)
        response = self.client.post(
            self._comments_url(),
            {"body": "m10-external-new", "visibility": PostComment.Visibility.EXTERNAL},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "m10-internal-root")
        self.assertContains(response, "m10-internal-reply")
        self.assertContains(response, "m10-external-new")

    def test_external_editor_can_download_internal_root_and_reply_by_uuid(self):
        self.client.force_login(self.external_editor)
        for comment, expected in (
            (self.internal_root, b"private-root-a"),
            (self.internal_reply, b"private-reply-a"),
        ):
            with self.subTest(comment=comment.id):
                response = self.client.get(self._attachment_url(self.ws_a, self.post_a, comment))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(b"".join(response.streaming_content), expected)

    def test_internal_editor_retains_legitimate_download_access(self):
        self.client.force_login(self.internal_editor)
        response = self.client.get(self._attachment_url(self.ws_a, self.post_a, self.internal_root))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"private-root-a")

    def test_client_observer_cannot_read_internal_root_reply_or_uuid(self):
        self.assertEqual(
            self._visible(self.observer),
            {"m10-external-root": ["m10-external-reply"]},
        )
        self.client.force_login(self.observer)
        for comment in (self.internal_root, self.internal_reply):
            with self.subTest(comment=comment.id):
                response = self.client.get(self._attachment_url(self.ws_a, self.post_a, comment))
                self.assertEqual(response.status_code, 404)
        public_response = self.client.get(self._attachment_url(self.ws_a, self.post_a, self.external_root))
        self.assertEqual(public_response.status_code, 200)
        self.assertEqual(b"".join(public_response.streaming_content), b"public-comment-a")

    def test_external_editor_cannot_download_b_or_c_without_membership(self):
        self.client.force_login(self.external_editor)
        for workspace, post, comment in (
            (self.ws_b, self.post_b, self.comment_b),
            (self.ws_c, self.post_c, self.comment_c),
        ):
            with self.subTest(workspace=workspace.id):
                response = self.client.get(self._attachment_url(workspace, post, comment))
                self.assertIn(response.status_code, (403, 404))

    def test_wrong_post_uuid_in_a_is_not_sufficient_to_download_comment(self):
        wrong_post = Post.objects.create(workspace=self.ws_a, author=self.internal_editor, caption="unrelated A")
        self.client.force_login(self.external_editor)
        response = self.client.get(self._attachment_url(self.ws_a, wrong_post, self.internal_root))
        self.assertEqual(response.status_code, 404)

    def test_downgrade_in_active_session_hides_internal_content_and_bytes(self):
        self.client.force_login(self.external_editor)
        membership = WorkspaceMembership.objects.get(user=self.external_editor, workspace=self.ws_a)
        membership.workspace_role = WorkspaceMembership.WorkspaceRole.CLIENT
        membership.save(update_fields=["workspace_role"])

        self.assertEqual(
            self._visible(self.external_editor),
            {"m10-external-root": ["m10-external-reply"]},
        )
        response = self.client.get(self._attachment_url(self.ws_a, self.post_a, self.internal_root))
        self.assertEqual(response.status_code, 404)
        rendered = self.client.post(self._comments_url(), {"body": "m10-after-downgrade"})
        self.assertEqual(rendered.status_code, 200)
        self.assertNotContains(rendered, "m10-internal-root")
        self.assertNotContains(rendered, "m10-internal-reply")

    def test_revoked_workspace_membership_blocks_direct_uuid_in_active_session(self):
        self.client.force_login(self.external_editor)
        url = self._attachment_url(self.ws_a, self.post_a, self.internal_root)
        first = self.client.get(url)
        self.assertEqual(first.status_code, 200)
        WorkspaceMembership.objects.filter(user=self.external_editor, workspace=self.ws_a).delete()
        self.assertIn(self.client.get(url).status_code, (403, 404))
        # Finalize o streaming somente após a operação ORM no TestCase.
        self.assertEqual(b"".join(first.streaming_content), b"private-root-a")

    def test_external_editor_can_still_create_internal_comment_as_builtin_editor(self):
        # Characterization of the unresolved identity gap, NOT intended policy.
        self.client.force_login(self.external_editor)
        response = self.client.post(
            self._comments_url(),
            {
                "body": "m10-editor-internal-write",
                "visibility": PostComment.Visibility.INTERNAL,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            PostComment.objects.filter(
                post=self.post_a,
                body="m10-editor-internal-write",
                visibility=PostComment.Visibility.INTERNAL,
            ).exists()
        )
