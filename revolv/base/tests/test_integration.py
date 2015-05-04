from bs4 import BeautifulSoup
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django_webtest import WebTest
from revolv.base.utils import get_profile
from revolv.lib.testing import TestUserMixin, UserTestingMixin, WebTestMixin
from revolv.project.models import Project, ProjectUpdate


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


class AuthIntegrationTest(TestUserMixin, WebTest, UserTestingMixin):
    csrf_checks = False

    def assert_user_can_follow_change_password_flow(self, user, password):
        """Given a user and their current password, assert they can change it via the auth pages."""
        self.send_user_login_request(user, password, webtest=True)

        dash_resp = self.app.get("/dashboard/").maybe_follow()
        change_pass_resp = dash_resp.click(linkid="change_password_link").maybe_follow()
        form = change_pass_resp.forms["change_password_form"]
        form["old_password"] = password
        form["new_password1"] = "new_pass"
        form["new_password2"] = "new_pass_oops"

        # user did not enter passwords correctly: should not be authed
        form.submit().maybe_follow()
        self.app.get("/logout/")
        no_user_authed_resp = self.send_user_login_request(user, "new_pass", webtest=True).maybe_follow()
        self.assertNoUserAuthed(no_user_authed_resp)

        self.send_user_login_request(user, password, webtest=True)
        dash_resp = self.app.get("/dashboard/").maybe_follow()
        change_pass_resp = dash_resp.click(linkid="change_password_link").maybe_follow()
        form = change_pass_resp.forms["change_password_form"]
        form["old_password"] = password
        form["new_password1"] = "new_pass"
        form["new_password2"] = "new_pass"

        # user should now be authed
        form.submit().maybe_follow()
        self.app.get("/logout/")
        user_authed_resp = self.send_user_login_request(user, "new_pass", webtest=True).maybe_follow()
        self.assertEqual(user_authed_resp.status_code, 200)
        self.assertUserAuthed(user_authed_resp)

    def test_change_password_flow(self):
        """Test that donors, ambassadors, and admins can change their passwords."""
        user1, _ = self.create_new_user_with_password("some_donor", "some_password")
        self.assert_user_can_follow_change_password_flow(user1, "some_password")
        amb, _ = self.create_new_user_with_password("some_ambassador", "some_password", ambassador=True)
        self.assert_user_can_follow_change_password_flow(amb, "some_password")
        admin, _ = self.create_new_user_with_password("some_admin", "some_password", admin=True)
        self.assert_user_can_follow_change_password_flow(admin, "some_password")

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
    """Integration tests related to ambassador and admin functions for the dashboard."""
    csrf_checks = False

    def assert_logged_in_user_can_create_project_via_dashboard(self, tagline):
        """
        Assert that the user currently logged in can create a project from the
        dashboard. This method must provide a unique tagline for the project, so
        that the project can be checked as correctly created.
        """
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

    def test_admin_can_complete_and_incomplete_active_project(self):
        """
        Test that an admin user can use the dashboard to mark active projects as complete
        and mark complete projects as back to active.

        Creates an active project and an admin user, then runs through the flow of completing
        and incompleting (marking as active again) the project.
        """
        self.test_profile.make_administrator()
        self.send_test_user_login_request(webtest=True)
        project = Project.factories.active.create()

        dash_resp = self.app.get("/dashboard/").maybe_follow()
        self.assert_in_response_html(dash_resp, "project-status-%i-%s" % (project.id, Project.ACTIVE))
        completed_resp = dash_resp.forms["complete_form_%i" % project.pk].submit("_complete").maybe_follow()
        self.assertEqual(completed_resp.status_code, 200)
        self.assertEqual(Project.objects.get(id=project.pk).project_status, Project.COMPLETED)

        dash_resp = self.app.get("/dashboard/").maybe_follow()
        self.assert_in_response_html(dash_resp, "project-status-%i-%s" % (project.id, Project.COMPLETED))
        incompleted_resp = dash_resp.forms["incomplete_form_%i" % project.pk].submit("_incomplete").maybe_follow()
        self.assertEqual(incompleted_resp.status_code, 200)
        self.assertEqual(Project.objects.get(id=project.pk).project_status, Project.ACTIVE)

        dash_resp = self.app.get("/dashboard/").maybe_follow()
        self.assert_in_response_html(dash_resp, "project-status-%i-%s" % (project.id, Project.ACTIVE))

    def assert_can_post_update_for_project(self, user, password, project):
        """
        Assert that the given user, with the given password, can create a project
        update for the given project.
        """
        self.app.get("/logout/")
        update_count = project.updates.count()
        self.send_user_login_request(user, password, webtest=True)
        dash_resp = self.app.get("/dashboard/").maybe_follow()
        updates_resp = dash_resp.forms["post_project_updates_form_%i" % project.pk].submit().maybe_follow()
        edit_page_form = updates_resp.forms["project_update_form"]
        edit_page_form = self.fill_form_from_model(edit_page_form, ProjectUpdate.factories.base.build())
        post_update_resp = edit_page_form.submit().maybe_follow()
        self.assertEqual(post_update_resp.status_code, 200)
        self.assertEqual(project.updates.count(), update_count + 1)

    def test_post_updates_for_active_and_completed_projects(self):
        """
        Test that project updates can be added by an admin user and the ambassador that
        created the project, both when the project is active and completed.
        """
        amb_user = User.objects.create_user(username="amb", password="amb_pass")
        amb = get_profile(amb_user)
        amb.make_ambassador()
        admin_user = User.objects.create_user(username="admin", password="admin_pass")
        admin = get_profile(admin_user)
        admin.make_administrator()
        project = Project.factories.active.create(ambassador=amb)

        self.assert_can_post_update_for_project(amb_user, "amb_pass", project)
        self.assert_can_post_update_for_project(admin_user, "admin_pass", project)

        project.complete_project()

        self.assert_can_post_update_for_project(amb_user, "amb_pass", project)
        self.assert_can_post_update_for_project(admin_user, "admin_pass", project)

    def test_ambassador_cant_see_other_ambassadors_projects(self):
        """
        Test that one ambassador cannot see the projects on the dashboard created by
        another ambassador.

        Creates two ambassador users, creates a project for each of them, then checks
        that the dashboard for each of them does not contain a reference to the other's
        project.
        """
        amb1_user = User.objects.create_user(username="amb1", password="amb1_pass")
        amb2_user = User.objects.create_user(username="amb2", password="amb2_pass")
        amb1 = get_profile(amb1_user)
        amb2 = get_profile(amb2_user)
        amb1.make_ambassador()
        amb2.make_ambassador()
        project1 = Project.factories.drafted.create(ambassador=amb1)
        project2 = Project.factories.drafted.create(ambassador=amb2)

        self.send_user_login_request(amb1_user, "amb1_pass", webtest=True)
        dash_resp = self.app.get("/dashboard/").maybe_follow()
        self.assert_in_response_html(dash_resp, "project-%i" % project1.pk)
        self.assert_not_in_response_html(dash_resp, "project-%i" % project2.pk)

        self.app.get("/logout/")
        self.send_user_login_request(amb2_user, "amb2_pass", webtest=True)
        dash_resp = self.app.get("/dashboard/").maybe_follow()
        self.assert_in_response_html(dash_resp, "project-%i" % project2.pk)
        self.assert_not_in_response_html(dash_resp, "project-%i" % project1.pk)
