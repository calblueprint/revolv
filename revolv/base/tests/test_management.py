from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import Payment
from revolv.project.models import Project
from revolv.revolv_cms.models import MainPageSettings


class SeedTest(TestCase):
    def test_seed(self):
        """Test manage.py seed command does not error."""
        call_command("seed", quiet=True)

    def test_clear(self):
        """Test manage.py seed --clear does not error."""
        call_command("seed", clear=True, quiet=True)

    def test_single(self):
        """Test manage.py seed command can load only a single seed spec."""
        call_command("seed", spec="revolvuserprofile", quiet=True)
        self.assertEqual(Project.objects.count(), 0)

    def test_seed_then_clear(self):
        """
        Test that we can run manage.py seed --clear, then manage.py seed, then
        manage.py seed --clear again, and nothing will have changed in the database.
        """
        user_count = User.objects.count()
        profile_count = RevolvUserProfile.objects.count()
        project_count = Project.objects.count()
        payment_count = Payment.objects.count()

        call_command("seed", clear=True, quiet=True)
        call_command("seed", quiet=True)
        call_command("seed", clear=True, quiet=True)

        self.assertEqual(User.objects.count(), user_count)
        self.assertEqual(RevolvUserProfile.objects.count(), profile_count)
        self.assertEqual(Project.objects.count(), project_count)
        self.assertEqual(Payment.objects.count(), payment_count)

    def test_seed_cms_settings(self):
        """Assert the seed for the cms settings works."""
        call_command("seed", quiet=True)
        # for MainPageSettings, there can be only one, so we just want to assert
        # that it's there.
        self.assertEqual(MainPageSettings.objects.count(), 1)

    def test_cms_seed(self):
        """
        Test that the CMS seed specifically works without erroring.

        The CMS seeding is a little bit finnicky because the wagtail Page
        model is part of a treebeard tree, so we have to jump through some
        hoops to clear the seed data (see the docstrings for the CMSSeedSpec
        in revolv.page.manage.ment.commands.seed).

        We call seed, then clear, then seed again on the cms spec, and make sure it
        doesn't IntegrityError due to treebeard's internal tree constraints being
        violated.
        """
        call_command("seed", spec="revolvuserprofile", quiet=True)
        call_command("seed", spec="cms", quiet=True)
        call_command("seed", spec="cms", quiet=True, clear=True)
        call_command("seed", spec="cms", quiet=True)

    def test_list(self):
        """Test that the seed --list command does not actually seed any data."""
        user_count = User.objects.count()
        profile_count = RevolvUserProfile.objects.count()
        project_count = Project.objects.count()
        payment_count = Payment.objects.count()

        call_command("seed", list=True, quiet=True)

        self.assertEqual(User.objects.count(), user_count)
        self.assertEqual(RevolvUserProfile.objects.count(), profile_count)
        self.assertEqual(Project.objects.count(), project_count)
        self.assertEqual(Payment.objects.count(), payment_count)
