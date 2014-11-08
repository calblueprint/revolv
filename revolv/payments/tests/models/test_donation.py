from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from django_facebook.utils import get_user_model
from revolv.base.signals import create_profile_of_user
from revolv.payments.models import (Donation, PaymentInstrumentType,
                                    PaymentTransaction)
from revolv.project.models import Project


class DonationTest(TestCase):

    def test_donation_create(self):
        """Verify that we can create a donation."""
        # Variables for setup
        user = User(username='user1')
        project = Project()
        instrument_type = PaymentInstrumentType(name='test instrument')
        pt = PaymentTransaction(amount=10.00, user=user, payment_instrument_type=instrument_type)

        # Try instantiating the model
        donation = Donation(project=project, payment_transaction=pt)


class DonationManagerTest(TestCase):

    def setUp(self):
        post_save.disconnect(receiver=create_profile_of_user, sender=get_user_model())
        call_command('loaddata', 'user', 'revolvuserprofile', 'donation', 'payment_transaction', 'project')

    def tearDown(self):
        post_save.connect(create_profile_of_user, sender=get_user_model())

    def test_user_donations(self):
        """Verify that we can find donations by user"""
        user = User.objects.get(id=1)
        donations = Donation.objects.user_donations(user)
        self.assertEqual(len(donations), 2)
        self.assertEqual(donations[0].amount(), 50)
        self.assertEqual(donations[1].donor(), user)

    def test_donated_projects(self):
        """Verify that we can find user donated projects from donations"""
        user = User.objects.get(id=2)
        projects = Donation.objects.donated_projects(user)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].org_name, "Comoonity Dairy")
