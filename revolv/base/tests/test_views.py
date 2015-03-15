from django.contrib.auth.models import User
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.lib.testing import TestUserMixin, UserTestingMixin


class AuthPagesTestCase(UserTestingMixin, TestUserMixin, TestCase):
    SIGNIN_URL = "/signin/"
    LOGIN_URL = "/login/"
    LOGOUT_URL = "/logout/"
    SIGNUP_URL = "/signup/"
    HOME_URL = "/"

    def test_page_found(self):
        """Test that we can actually render a page."""
        response = self.client.get("/signin/")
        self.assertEqual(response.status_code, 200)

    def test_login_endpoint(self):
        """Test that the login endpoint correctly logs in a user."""
        response = self.send_test_user_login_request()
        self.assertEqual(response.context["user"], self.test_user)
        self.assertUserAuthed(response)

    def test_garbage_login(self):
        response = self.client.post(self.LOGIN_URL, {
            "username": "hjksadhfiobhv",
            "password": "njnpvbebijrwehgjsd"
        }, follow=True)
        self.assertTemplateUsed(response, "base/sign_in.html")
        self.assertNoUserAuthed(response)

    def test_login_logout(self):
        """
        Test that after logging in, the user object can be correctly
        logged out.
        """
        self.send_test_user_login_request()
        response = self.client.get(self.SIGNIN_URL, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        response = self.client.get(self.LOGIN_URL, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        response = self.client.get(self.LOGOUT_URL, follow=True)
        self.assertNoUserAuthed(response)

    def test_signup_endpoint(self):
        """Test that we can create a new user through the signup form."""
        valid_data = {
            "username": "john123",
            "password1": "doe_password_1",
            "password2": "doe_password_1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "subscribed_to_newsletter": True
        }

        no_name_data = valid_data.copy()
        no_name_data["first_name"] = ""

        no_email_data = valid_data.copy()
        no_email_data["email"] = ""

        response = self.client.post(self.SIGNUP_URL, no_name_data, follow=True)  # maybe SIGNIN_URL instead?
        self.assertTemplateUsed(response, "base/sign_in.html")
        self.assertNoUserAuthed(response)

        response = self.client.post(self.SIGNUP_URL, no_email_data, follow=True)
        self.assertTemplateUsed(response, "base/sign_in.html")
        self.assertNoUserAuthed(response)

        response = self.client.post(self.SIGNUP_URL, valid_data, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        self.assertUserAuthed(response)

        # make sure the user was actually saved
        test_user = User.objects.get(username="john123")
        RevolvUserProfile.objects.get(user=test_user)
