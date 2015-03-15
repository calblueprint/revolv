from bs4 import BeautifulSoup
from django.contrib.auth import authenticate
from django.core import mail
from django.test import TestCase
from django_webtest import WebTest
from revolv.lib.testing import TestUserMixin


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
