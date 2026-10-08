"""Tests for client portal magic-link single-use enforcement."""

from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.approvals.models import PostComment
from apps.client_portal.models import MagicLinkToken
from apps.client_portal.services import consume_magic_link, peek_magic_link
from apps.composer.models import PlatformPost, Post
from apps.members.models import WorkspaceMembership
from apps.organizations.models import Organization
from apps.social_accounts.models import SocialAccount
from apps.workspaces.models import Workspace


class MagicLinkTestBase(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Test Org")
        self.workspace = Workspace.objects.create(organization=self.org, name="Test Workspace")
        self.client_user = User.objects.create_user(
            email="client@example.com",
            password="testpass123",
            tos_accepted_at=timezone.now(),
        )
        WorkspaceMembership.objects.create(
            user=self.client_user,
            workspace=self.workspace,
            workspace_role=WorkspaceMembership.WorkspaceRole.CLIENT,
        )
        self.token = MagicLinkToken.objects.create(user=self.client_user, workspace=self.workspace)

    def _expire(self, token):
        token.expires_at = timezone.now() - timedelta(days=1)
        token.save(update_fields=["expires_at"])


class PeekMagicLinkTests(MagicLinkTestBase):
    def test_peek_returns_token_for_fresh_token(self):
        self.assertEqual(peek_magic_link(self.token.token), self.token)

    def test_peek_does_not_consume_token(self):
        peek_magic_link(self.token.token)
        self.token.refresh_from_db()
        self.assertFalse(self.token.is_consumed)

    def test_peek_returns_none_for_expired_token(self):
        self._expire(self.token)
        self.assertIsNone(peek_magic_link(self.token.token))

    def test_peek_returns_none_for_consumed_token(self):
        self.token.is_consumed = True
        self.token.save(update_fields=["is_consumed"])
        self.assertIsNone(peek_magic_link(self.token.token))

    def test_peek_returns_none_for_unknown_token(self):
        self.assertIsNone(peek_magic_link("does-not-exist"))


class ConsumeMagicLinkTests(MagicLinkTestBase):
    def test_consume_first_use_succeeds_and_marks_consumed(self):
        user, workspace, is_valid = consume_magic_link(self.token.token)
        self.assertTrue(is_valid)
        self.assertEqual(user, self.client_user)
        self.assertEqual(workspace, self.workspace)
        self.token.refresh_from_db()
        self.assertTrue(self.token.is_consumed)
        self.assertIsNotNone(self.token.last_used_at)

    def test_consume_second_use_is_rejected(self):
        consume_magic_link(self.token.token)
        self.assertEqual(consume_magic_link(self.token.token), (None, None, False))

    def test_consume_expired_token_is_rejected(self):
        self._expire(self.token)
        self.assertEqual(consume_magic_link(self.token.token), (None, None, False))

    def test_consume_unknown_token_is_rejected(self):
        self.assertEqual(consume_magic_link("does-not-exist"), (None, None, False))


class MagicLinkEntryViewTests(MagicLinkTestBase):
    def _entry_url(self, token=None):
        return reverse("client_portal:magic_link_entry", kwargs={"token": token or self.token.token})

    def test_get_renders_confirmation_without_consuming(self):
        response = self.client.get(self._entry_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "client_portal/magic_link_confirm.html")
        self.token.refresh_from_db()
        self.assertFalse(self.token.is_consumed)

    def test_get_with_consumed_token_redirects_to_expired(self):
        self.token.is_consumed = True
        self.token.save(update_fields=["is_consumed"])
        response = self.client.get(self._entry_url())
        self.assertRedirects(response, reverse("client_portal:magic_link_expired"))

    def test_post_consumes_token_and_starts_session(self):
        response = self.client.post(self._entry_url())
        self.assertRedirects(
            response,
            reverse("client_portal:dashboard"),
            fetch_redirect_response=False,
        )
        self.token.refresh_from_db()
        self.assertTrue(self.token.is_consumed)
        self.assertTrue(self.client.session.get("is_portal_session"))

    def test_post_twice_rejects_the_reused_token(self):
        self.client.post(self._entry_url())
        # A fresh client simulates the link being replayed by someone else.
        replay = Client()
        response = replay.post(self._entry_url())
        self.assertRedirects(response, reverse("client_portal:magic_link_expired"))
        self.assertIsNone(replay.session.get("is_portal_session"))


class PortalInternalCommentVisibilityTests(MagicLinkTestBase):
    """Portal never reveals team-only comments, even after role changes."""

    def setUp(self):
        super().setUp()
        self.account = SocialAccount.objects.create(
            workspace=self.workspace,
            platform="linkedin_personal",
            account_platform_id="synthetic-portal-page",
            account_name="Synthetic Social Page",
            connection_status=SocialAccount.ConnectionStatus.CONNECTED,
        )
        self.post = Post.objects.create(
            workspace=self.workspace,
            author=self.client_user,
            caption="Visible post caption",
        )
        PlatformPost.objects.create(
            post=self.post,
            social_account=self.account,
            status="pending_client",
        )
        PostComment.objects.create(
            post=self.post,
            author=self.client_user,
            body="team-secret-internal-note",
            visibility=PostComment.Visibility.INTERNAL,
        )
        PostComment.objects.create(
            post=self.post,
            author=self.client_user,
            body="client-visible-external-note",
            visibility=PostComment.Visibility.EXTERNAL,
        )
        self.client.force_login(self.client_user)
        session = self.client.session
        session["is_portal_session"] = True
        session["portal_workspace_id"] = str(self.workspace.id)
        session.save()

    def test_client_role_sees_only_external_comments(self):
        response = self.client.get(reverse("client_portal:approval_queue"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "client-visible-external-note")
        self.assertNotContains(response, "team-secret-internal-note")

    def test_editor_role_in_active_portal_session_still_sees_only_external_comments(self):
        membership = WorkspaceMembership.objects.get(user=self.client_user, workspace=self.workspace)
        membership.workspace_role = WorkspaceMembership.WorkspaceRole.EDITOR
        membership.save(update_fields=["workspace_role"])

        response = self.client.get(reverse("client_portal:approval_queue"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "client-visible-external-note")
        self.assertNotContains(response, "team-secret-internal-note")

    def test_internal_reply_to_external_comment_is_not_prefetched(self):
        parent = PostComment.objects.get(
            post=self.post,
            body="client-visible-external-note",
        )
        PostComment.objects.create(
            post=self.post,
            parent_comment=parent,
            author=self.client_user,
            body="team-secret-internal-reply",
            visibility=PostComment.Visibility.INTERNAL,
        )
        response = self.client.get(reverse("client_portal:approval_queue"))
        self.assertEqual(response.status_code, 200)
        visible = response.context["pending_posts"][0].visible_comments
        self.assertEqual([comment.body for comment in visible], ["client-visible-external-note"])
        self.assertEqual(list(visible[0].replies.all()), [])
        self.assertNotContains(response, "team-secret-internal-reply")

    def test_session_cannot_switch_to_unjoined_workspace(self):
        foreign = Workspace.objects.create(name="Unjoined Client", organization=self.workspace.organization)
        session = self.client.session
        session["portal_workspace_id"] = str(foreign.id)
        session.save()
        response = self.client.get(reverse("client_portal:approval_queue"))
        self.assertRedirects(response, reverse("client_portal:magic_link_expired"))
