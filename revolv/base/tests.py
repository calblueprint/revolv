from django.contrib.auth.models import User
from django.test import TestCase
from revolv.base.models import RevolvUserProfile


class SmokeTestCase(TestCase):
    def test_works(self):
        """Test that the test framework works."""
        self.assertEqual(1, 1)


class UserAuthTestCase(TestCase):
    def test_user_profile_sync(self):
        """
        Test that saving/deleting a User will get/create/delete the
        appropriate user profile as well.
        """
        test_user = User.objects.create_user(
            "John",
            "john@example.com",
            "password"
        )
        profile = RevolvUserProfile.objects.filter(user=test_user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile, test_user.revolvuserprofile)

        test_user.last_name = "Doe"
        test_user.save()

        profiles = RevolvUserProfile.objects.filter(user=test_user)
        self.assertEqual(len(profiles), 1)

        test_user.delete()
        profile = RevolvUserProfile.objects.filter(user=test_user).first()
        self.assertIsNone(profile)


class LoginSignupPageTestCase(TestCase):
    def test_page_found(self):
        """Test that we can actually render a page."""
        response = self.client.get("/signin/")
        self.assertEqual(response.status_code, 200)
