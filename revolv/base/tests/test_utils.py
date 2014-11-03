from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.base.utils import (get_all_administrator_emails,
                               get_all_administrators)


class AdminUtilsTestCase(TestCase):
    def setUp(self):
        self.admin1 = RevolvUserProfile.objects.create_user_as_admin(
            "admin1",
            "admin1@revolv.org",
            "admin1pass"
        )
        self.admin2 = RevolvUserProfile.objects.create_user_as_admin(
            "admin2",
            "admin2@revolv.org",
            "admin2pass"
        )
        self.admin3 = RevolvUserProfile.objects.create_user_as_admin(
            "admin3",
            "admin3@revolv.org",
            "admin3pass"
        )

    def test_get_admins(self):
        admins = get_all_administrators().all()
        self.assertEquals(len(admins), 3)
        self.assertIn(self.admin1.user, admins)
        self.assertIn(self.admin2.user, admins)
        self.assertIn(self.admin3.user, admins)

    def test_get_admin_emails(self):
        emails = get_all_administrator_emails()
        self.assertIn("admin1@revolv.org", emails)
        self.assertIn("admin2@revolv.org", emails)
        self.assertIn("admin3@revolv.org", emails)
