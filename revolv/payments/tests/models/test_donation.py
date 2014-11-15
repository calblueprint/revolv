from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from django_facebook.utils import get_user_model
from revolv.base.signals import create_profile_of_user
from revolv.payments.models import Donation


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
