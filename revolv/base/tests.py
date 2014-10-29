from django.contrib.auth.models import User
from django.test import TestCase
from revolv.base.models import RevolvUserProfile


class SmokeTestCase(TestCase):
    def test_works(self):
        """Test that the test framework works."""
        self.assertEqual(1, 1)


class UserAuthTestCase(TestCase):
    def setUp(self):
        """Every test in this case has a test user."""
        self.test_user = User.objects.create_user(
            "John",
            "john@example.com",
            "test_user_password"
        )

    def test_user_profile_sync(self):
        """
        Test that saving/deleting a User will get/create/delete the
        appropriate user profile as well.

        Note: django 1.7 removes support for user.get_profile(), so we test
        here that we can access a user's profile using user.revolvuserprofile.
        """
        profile = RevolvUserProfile.objects.filter(user=self.test_user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile, self.test_user.revolvuserprofile)

        self.test_user.last_name = "Doe"
        self.test_user.save()

        profiles = RevolvUserProfile.objects.filter(user=self.test_user)
        self.assertEqual(len(profiles), 1)

        self.test_user.delete()
        profile = RevolvUserProfile.objects.filter(user=self.test_user).first()
        self.assertIsNone(profile)

    def test_login_endpoint(self):
        """Test that the login endpoint correctly logs in a user."""
        response = self.client.post(
            "/login/",
            {
                "username": self.test_user.get_username(),
                "password": "test_user_password"
            },
            follow=True
        )
        self.assertEqual(response.context["user"], self.test_user)


class LoginSignupPageTestCase(TestCase):
    def test_page_found(self):
        """Test that we can actually render a page."""
        response = self.client.get("/signin/")
        self.assertEqual(response.status_code, 200)
