from bs4 import BeautifulSoup
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django_webtest import WebTest
from revolv.base.utils import get_profile
from revolv.lib.testing import TestUserMixin, WebTestMixin
from revolv.project.models import Project


class DashboardTestCase(TestUserMixin, TestCase):
    DASH_BASE = "/dashboard/"
    ADMIN_DASH = "/dashboard/admin/"
    AMBAS_DASH = "/dashboard/ambassador/"
    DONOR_DASH = "/dashboard/donor/"
    HOME_URL = "/"

    def test_dash_redirects(self):
        """Test that the dashboard links redirect to the correct dashboard levels."""
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.HOME_URL)

        self.send_test_user_login_request()
        self.test_profile.make_administrator()
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.ADMIN_DASH)

        self.test_profile.make_ambassador()
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.AMBAS_DASH)

        self.test_profile.make_donor()
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.DONOR_DASH)


class AuthIntegrationTest(TestUserMixin, WebTest):
    def test_forgot_password_flow(self):
        """Test that the entire forgot password flow works."""
        response = self.app.get("/login/").maybe_follow()
        reset_page_response = response.click(linkid="reset").maybe_follow()
        self.assertTemplateUsed(reset_page_response, "base/auth/forgot_password_initial.html")

        form = reset_page_response.forms["password_reset_form"]
        self.assertEqual(form.method, "post")

        # email should not be sent if we don't have a user with that email
        form["email"] = "something@idontexist.com"
        unregistered_email_response = form.submit().maybe_follow()
        self.assertTemplateUsed(unregistered_email_response, "base/auth/forgot_password_done.html")
        self.assertEqual(len(mail.outbox), 0)

        form["email"] = self.test_user.email
        registered_email_response = form.submit().maybe_follow()
        self.assertTemplateUsed(registered_email_response, "base/auth/forgot_password_done.html")
        self.assertEqual(len(mail.outbox), 1)

        query = BeautifulSoup(mail.outbox[0].body)
        # we want to make sure that there is a password reset link (not just a url) in the email
        link = query.find(id="reset_password_link")
        self.assertIsNotNone(link)

        confirm_url = link["href"]
        confirm_response = self.app.get(confirm_url).maybe_follow()
        self.assertEqual(confirm_response.context["validlink"], True)

        form = confirm_response.forms["password_reset_confirm_form"]
        form["new_password1"] = "test_new_password"
        form["new_password2"] = "test_new_password"
        success_response = form.submit().maybe_follow()
        self.assertEqual(success_response.status_code, 200)
        self.bust_test_user_cache()
        result = authenticate(username=self.test_user.username, password="test_new_password")
        self.assertEqual(result, self.test_user)


class DashboardIntegrationTest(TestUserMixin, WebTest, WebTestMixin):
    csrf_checks = False

    def assert_logged_in_user_can_create_project_via_dashboard(self, tagline):
        project = Project.factories.base.build(tagline=tagline)

        dashboard_response = self.app.get("/dashboard/").maybe_follow()
        create_page_response = dashboard_response.click(linkid="create_project").maybe_follow()
        project_form = create_page_response.forms["project_form"]
        project_form = self.fill_form_from_model(project_form, project)
        dashboard_new_project_response = project_form.submit().maybe_follow()
        self.assertEqual(dashboard_new_project_response.status_code, 200)

        created_project = Project.objects.get(tagline=tagline)
        self.assertEqual(created_project.project_status, Project.DRAFTED)
        self.assert_in_response_html(dashboard_new_project_response, "project-%d" % created_project.pk)

    def test_create_new_project_via_dashboard(self):
        """Test that an ambassador can create a new project via the dashboard."""
        self.test_profile.make_ambassador()
        self.send_test_user_login_request(webtest=True)

        self.assert_logged_in_user_can_create_project_via_dashboard("this_project_made_by_ambsaddador")

        self.test_profile.make_administrator()
        self.send_test_user_login_request(webtest=True)
        self.assert_logged_in_user_can_create_project_via_dashboard("this_project_made_by_admin")

    def test_ambassador_can_propose_project(self):
        """
        Test that if an ambassador has created a project, it will show up on the dashboard
        and they can propose it from there.

        Note: this is a possible failure point if we scale the RE-volv app to many projects,
        and change the dashboard to load project asynchronously: this async loading could cause
        the test to fail because it won't find the project propose button.
        """
        self.test_profile.make_ambassador()
        self.send_test_user_login_request(webtest=True)

        project = Project.factories.drafted.create(ambassador=self.test_profile)
        dash_response = self.app.get("/dashboard/").maybe_follow()
        propose_form = dash_response.forms["propose_form_%i" % project.pk]
        new_dash_response = propose_form.submit("_propose").maybe_follow()
        self.assertEqual(new_dash_response.status_code, 200)

        self.assertEqual(Project.objects.get(id=project.pk).project_status, Project.PROPOSED)

    def test_admin_can_approve_or_deny_proposed_project(self):
        """
        Test that an admin can approve and deny proposed projects from the dashboard.

        Creates two projects, both proposed, and tests that the admin can use the buttons
        on the dashboard to approve and deny, respectively, each one. Then, tests that
        the ambassador that created the projects can see
        """
        amb_user = User.objects.create_user(username="amb", password="amb_pass")
        admin_user = User.objects.create_user(username="admin", password="admin_pass")
        ambassador = get_profile(amb_user)
        admin = get_profile(admin_user)
        ambassador.make_ambassador()
        admin.make_administrator()
        project1 = Project.factories.proposed.create(ambassador=ambassador)
        project2 = Project.factories.proposed.create(ambassador=ambassador)

        self.send_user_login_request(admin_user, "admin_pass", webtest=True)
        dash_resp = self.app.get("/dashboard/").maybe_follow()
        approved_resp = dash_resp.forms["approve_deny_form_%i" % project1.pk].submit("_approve").maybe_follow()
        self.assertEqual(approved_resp.status_code, 200)
        # TODO(#255): when we add a STAGED project status as per https://github.com/calblueprint/revolv/issues/255,
        # we'll need to check that project 1 is staged here instead of active.
        self.assertEqual(Project.objects.get(id=project1.pk).project_status, Project.ACTIVE)

        denied_resp = dash_resp.forms["approve_deny_form_%i" % project2.pk].submit("_deny").maybe_follow()
        self.assertEqual(denied_resp.status_code, 200)
        self.assertEqual(Project.objects.get(id=project2.pk).project_status, Project.DRAFTED)

        self.app.get("/logout/")
        self.send_user_login_request(amb_user, "amb_pass", webtest=True)
        amb_dash_resp = self.app.get("/dashboard/").maybe_follow()
        self.assert_in_response_html(amb_dash_resp, "project-status-%i-%s" % (project1.pk, Project.ACTIVE))
        self.assert_in_response_html(amb_dash_resp, "project-status-%i-%s" % (project2.pk, Project.DRAFTED))

    def test_admin_can_complete_active_project(self):
        pass

    def test_post_updates_for_active_and_completed_projects(self):
        pass

    def test_ambassador_cant_see_other_ambassadors_projects(self):
        pass
