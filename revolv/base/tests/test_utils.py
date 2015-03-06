from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.base.utils import (get_all_administrator_emails,
                               get_all_administrators)


class AdminUtilsTestCase(TestCase):
    def test_get_admins(self):
        """Test that we can retrive a query of all the admin users."""
        admins_profiles = RevolvUserProfile.factories.admin.create_batch(3)
        db_admins = get_all_administrators().all()
        self.assertEquals(len(db_admins), 3)
        for admin in admins_profiles:
            self.assertIn(admin.user, db_admins)

    def test_get_admin_emails(self):
        """Test that we can batch retrive all admin user emails."""
        admins = RevolvUserProfile.factories.admin.create_batch(3)
        emails = get_all_administrator_emails()
        for admin in admins:
            self.assertIn(admin.user.email, emails)
