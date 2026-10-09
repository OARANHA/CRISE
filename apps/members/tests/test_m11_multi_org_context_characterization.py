"""M11: characterize multi-organization context without changing BrightBean policy.

The VIGIAFAST tenant decision (ADR-0003) is NOT accepted. These tests use
only synthetic fixtures. A passing test documents the *current* middleware
behavior, not a claim that a multi-organization rollout is safe.
"""

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.members.middleware import RBACMiddleware
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace


def _synthetic_operator():
    user = User.objects.create_user(
        email="m11-multi-org-operator@example.invalid",
        password="synthetic-test-password",
        tos_accepted_at=timezone.now(),
    )
    # Account signals create a personal org/workspace; remove only those
    # auto-created rows to isolate the two synthetic organizations below.
    auto_org_ids = list(OrgMembership.objects.filter(user=user).values_list("organization_id", flat=True))
    WorkspaceMembership.objects.filter(user=user).delete()
    OrgMembership.objects.filter(user=user).delete()
    Organization.objects.filter(id__in=auto_org_ids).delete()
    user.last_workspace_id = None
    user.save(update_fields=["last_workspace_id"])
    return user


class MultiOrgContextCharacterizationTests(TestCase):
    """An operator can have two org memberships, but global context picks one."""

    @classmethod
    def setUpTestData(cls):
        cls.org_a = Organization.objects.create(name="M11 Synthetic Organization A")
        cls.org_b = Organization.objects.create(name="M11 Synthetic Organization B")
        cls.ws_a = Workspace.objects.create(organization=cls.org_a, name="M11 Synthetic Workspace A")
        cls.ws_b = Workspace.objects.create(organization=cls.org_b, name="M11 Synthetic Workspace B")
        cls.ws_b_unassigned = Workspace.objects.create(
            organization=cls.org_b, name="M11 Synthetic Unassigned Workspace"
        )
        cls.operator = _synthetic_operator()
        for org, ws in ((cls.org_a, cls.ws_a), (cls.org_b, cls.ws_b)):
            OrgMembership.objects.create(user=cls.operator, organization=org, org_role=OrgMembership.OrgRole.MEMBER)
            WorkspaceMembership.objects.create(
                user=cls.operator,
                workspace=ws,
                workspace_role=WorkspaceMembership.WorkspaceRole.EDITOR,
            )

    @staticmethod
    def _middleware():
        return RBACMiddleware(lambda request: HttpResponse("synthetic-ok"))

    def _global_request(self, path="/notifications/"):
        request = RequestFactory().get(path)
        request.user = self.operator
        response = self._middleware()(request)
        self.assertEqual(response.status_code, 200)
        return request

    def test_global_org_can_disagree_with_current_workspace_for_multi_org_actor(self):
        first_membership = OrgMembership.objects.filter(user=self.operator).first()
        self.assertIsNotNone(first_membership)
        selected_workspace = self.ws_b if first_membership.organization_id == self.org_a.id else self.ws_a
        self.operator.last_workspace_id = selected_workspace.id
        self.operator.save(update_fields=["last_workspace_id"])

        request = self._global_request()

        self.assertEqual(request.workspace.id, selected_workspace.id)
        self.assertEqual(request.org.id, first_membership.organization_id)
        self.assertNotEqual(request.org.id, request.workspace.organization_id)

    def test_explicit_workspace_url_resolves_its_organization_and_membership(self):
        request = self._global_request()
        middleware = self._middleware()

        result = middleware.process_view(
            request,
            lambda req, **kwargs: HttpResponse("synthetic-view"),
            (),
            {"workspace_id": self.ws_b.id},
        )

        self.assertIsNone(result)
        self.assertEqual(request.workspace.id, self.ws_b.id)
        self.assertEqual(request.org.id, self.org_b.id)
        self.assertEqual(request.org_membership.organization_id, self.org_b.id)
        self.assertEqual(request.workspace_membership.user_id, self.operator.id)

    def test_other_workspace_in_same_organization_still_requires_membership(self):
        request = self._global_request()
        middleware = self._middleware()

        with self.assertRaises(PermissionDenied):
            middleware.process_view(
                request,
                lambda req, **kwargs: HttpResponse("synthetic-view"),
                (),
                {"workspace_id": self.ws_b_unassigned.id},
            )

    def test_workspace_membership_revocation_is_rechecked_by_process_view(self):
        request = self._global_request()
        middleware = self._middleware()
        kwargs = {"workspace_id": self.ws_b.id}

        middleware.process_view(request, lambda req, **kw: HttpResponse("ok"), (), kwargs)
        self.assertEqual(request.workspace.id, self.ws_b.id)

        WorkspaceMembership.objects.filter(user=self.operator, workspace=self.ws_b).delete()
        with self.assertRaises(PermissionDenied):
            middleware.process_view(request, lambda req, **kw: HttpResponse("ok"), (), kwargs)
