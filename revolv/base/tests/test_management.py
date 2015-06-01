from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import Payment
from revolv.project.models import Project


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
