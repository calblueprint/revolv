from django.contrib.auth.models import User
from django.test import TestCase
from revolv.base.models import RevolvUserProfile


class SmokeTestCase(TestCase):
    def test_works(self):
        """Test that the test framework works."""
        self.assertEqual(1, 1)


class UserAuthTestCase(TestCase):
    def test_user_profile_sync(self):
        test_user = User.objects.create_user(
            "John",
            "john@example.com",
            "password"
        )
        profile = RevolvUserProfile.objects.filter(user=test_user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile, test_user.revolvuserprofile)

        test_user.delete()
        profile = RevolvUserProfile.objects.filter(user=test_user).first()
        self.assertIsNone(profile)
