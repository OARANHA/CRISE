"""HTTP regressions for cross-client exposure in the organization directory.

All actors, e-mails and workspaces are synthetic. These are red-first security
assertions: they are intended to expose the current /members/ behavior before
any authorization policy is changed. Never run against production.
"""

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.members.models import OrgMembership, WorkspaceMembership
from apps.organizations.models import Organization
from apps.workspaces.models import Workspace


def _synthetic_user(email, name):
    user = User.objects.create_user(
        email=email,
        name=name,
        password="synthetic-test-only-password",
        tos_accepted_at=timezone.now(),
    )
    # User provisioning signals create a personal org/workspace by default.
    # Remove only this freshly created fixture data so global RBAC context
    # resolves deterministically to the organizations used in these tests.
    auto_org_memberships = OrgMembership.objects.filter(user=user)
    auto_org_ids = list(auto_org_memberships.values_list("organization_id", flat=True))
    WorkspaceMembership.objects.filter(user=user).delete()
    OrgMembership.objects.filter(user=user).delete()
    Organization.objects.filter(id__in=auto_org_ids).delete()
    user.last_workspace_id = None
    user.save(update_fields=["last_workspace_id"])
    return user


class OrgDirectoryClientIsolationTests(TestCase):
    """T01/T10: O1 contains clients A and B; O2 contains client C."""

    @classmethod
    def setUpTestData(cls):
        cls.org_o1 = Organization.objects.create(name="SYNTHETIC_ORG_O1")
        cls.org_o2 = Organization.objects.create(name="SYNTHETIC_ORG_O2")
        cls.ws_a = Workspace.objects.create(organization=cls.org_o1, name="SYNTHETIC_WS_A")
        cls.ws_b = Workspace.objects.create(organization=cls.org_o1, name="SYNTHETIC_WS_B_PRIVATE")
        cls.ws_c = Workspace.objects.create(organization=cls.org_o2, name="SYNTHETIC_WS_C_PRIVATE")

        cls.owner = cls._member("owner@example.invalid", "O1 Owner", cls.org_o1, "owner")
        cls.admin = cls._member("admin@example.invalid", "O1 Administrator", cls.org_o1, "admin")
        cls.observer_a = cls._member(
            "observer-a@example.invalid",
            "Observer A",
            cls.org_o1,
            "member",
            [(cls.ws_a, "client")],
        )
        cls.operator_a = cls._member(
            "operator-a@example.invalid",
            "Operator A",
            cls.org_o1,
            "member",
            [(cls.ws_a, "editor")],
        )
        cls.client_b = cls._member(
            "client-b-secret@example.invalid",
            "CLIENT_B_PRIVATE_IDENTITY",
            cls.org_o1,
            "member",
            [(cls.ws_b, "client")],
        )
        cls.client_c = cls._member(
            "client-c-secret@example.invalid",
            "CLIENT_C_PRIVATE_IDENTITY",
            cls.org_o2,
            "member",
            [(cls.ws_c, "client")],
        )
        cls.internal_ab = cls._member(
            "internal-ab@example.invalid",
            "Internal A B Operator",
            cls.org_o1,
            "member",
            [(cls.ws_a, "editor"), (cls.ws_b, "editor")],
        )
        cls.no_membership = _synthetic_user("unaffiliated@example.invalid", "Unaffiliated")

    @staticmethod
    def _member(email, name, org, org_role, assignments=()):
        user = _synthetic_user(email, name)
        OrgMembership.objects.create(organization=org, user=user, org_role=org_role)
        for workspace, workspace_role in assignments:
            WorkspaceMembership.objects.create(user=user, workspace=workspace, workspace_role=workspace_role)
        return user

    def setUp(self):
        self.list_url = reverse("members:list")

    def _get_directory(self, user=None, *, htmx=False):
        self.client.logout()
        if user is not None:
            self.client.force_login(user)
        headers = {"HTTP_HX_REQUEST": "true"} if htmx else {}
        return self.client.get(self.list_url, **headers)

    def _assert_client_b_hidden(self, response):
        # Denying the entire directory is acceptable as a confidentiality
        # boundary; if a scoped directory is served, scope its query and HTML.
        self.assertIn(response.status_code, (200, 403, 404))
        if response.status_code == 200:
            self.assertNotContains(response, self.client_b.email)
            self.assertNotContains(response, self.client_b.display_name)
            self.assertNotContains(response, self.ws_b.name)
            exposed_ids = [member["user"].pk for member in response.context["members_data"]]
            self.assertNotIn(self.client_b.pk, exposed_ids)

    def test_observer_a_must_not_see_b_name_email_or_workspace(self):
        response = self._get_directory(self.observer_a)
        self._assert_client_b_hidden(response)

    def test_operator_editor_a_must_not_inherit_org_wide_directory(self):
        response = self._get_directory(self.operator_a)
        self._assert_client_b_hidden(response)

    def test_htmx_request_must_not_expose_client_b(self):
        response = self._get_directory(self.observer_a, htmx=True)
        self._assert_client_b_hidden(response)

    def test_revoked_workspace_access_must_not_expose_client_b(self):
        WorkspaceMembership.objects.filter(user=self.observer_a, workspace=self.ws_a).delete()
        # Keep the org membership, reproducing a partial offboarding path.
        response = self._get_directory(self.observer_a)
        self._assert_client_b_hidden(response)

    def test_other_organization_member_cannot_see_o1_directory(self):
        response = self._get_directory(self.client_c)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.client_c.email)
        self.assertNotContains(response, self.client_b.email)
        self.assertNotContains(response, self.ws_b.name)

    def test_internal_user_assigned_to_a_and_b_keeps_directory_access(self):
        response = self._get_directory(self.internal_ab)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ws_a.name)
        self.assertContains(response, self.ws_b.name)
        self.assertNotContains(response, self.client_c.email)

    def test_observer_a_does_not_see_b_via_shared_internal_member_badge(self):
        response = self._get_directory(self.observer_a)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.internal_ab.email)
        self.assertContains(response, self.ws_a.name)
        self.assertNotContains(response, self.ws_b.name)
        self.assertQuerySetEqual(
            response.context["org_workspaces"],
            [self.ws_a],
        )

    def test_member_without_workspace_sees_only_own_identity(self):
        member = self._member("unassigned@example.invalid", "No Workspace", self.org_o1, "member")
        response = self._get_directory(member)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, member.email)
        self.assertNotContains(response, self.client_b.email)
        self.assertNotContains(response, self.ws_b.name)
        self.assertEqual(len(response.context["members_data"]), 1)
        self.assertEqual(response.context["members_data"][0]["user"].pk, member.pk)

    def test_org_owner_can_manage_all_members(self):
        response = self._get_directory(self.owner)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.client_b.email)
        self.assertContains(response, self.ws_b.name)

    def test_org_admin_can_manage_all_members(self):
        response = self._get_directory(self.admin)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.client_b.email)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self._get_directory()
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_user_without_any_org_membership_is_denied(self):
        response = self._get_directory(self.no_membership)
        self.assertEqual(response.status_code, 403)

    def test_client_editor_cannot_open_other_member_workspace_form(self):
        self.client.force_login(self.operator_a)
        membership = OrgMembership.objects.get(user=self.client_b, organization=self.org_o1)
        url = reverse("members:manage_workspaces", kwargs={"membership_id": membership.pk})
        response = self.client.get(url, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 403)

    def test_client_observer_cannot_change_other_member_org_role(self):
        self.client.force_login(self.observer_a)
        membership = OrgMembership.objects.get(user=self.client_b, organization=self.org_o1)
        url = reverse("members:update_role", kwargs={"membership_id": membership.pk})
        response = self.client.post(url, {"org_role": "admin"}, HTTP_HX_REQUEST="true")
        self.assertEqual(response.status_code, 403)
