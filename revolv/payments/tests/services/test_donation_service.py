import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from revolv.payments.models import PaymentInstrumentType, PaymentTransaction
from revolv.payments.services import DonationService
from revolv.project.models import Project


class DonationServiceTest(TestCase):

    fixtures = ['supported_instruments.json']

    def setUp(self):
        self.user = User(username='billnye')
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        self.project = Project(
            funding_goal=20.0,
            title="Hello",
            video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
            impact_power=50.5,
            location="San Francisco",
            end_date=tomorrow,
            mission_statement="Blueprint!",
            cover_photo="http://i.imgur.com/2zMTZgi.jpg",
            org_start_date=yesterday,
            actual_energy=25.5,
            amount_repaid=29.25,
            ambassador_id=1,
        )
        self.project.save()
        self.user.save()
        self.payment_transaction = PaymentTransaction(
            amount=10.00, user=self.user, payment_instrument_type=PaymentInstrumentType.objects.get(name='paypal'))
        self.payment_transaction.save()
        self.donation = None

    def tearDown(self):
        if self.donation:
            self.donation.delete()

        self.user.delete()
        self.project.delete()
        self.payment_transaction.delete()

    def test_create_donation_service(self):
        """Verify that we can create a donation through the service."""
        self.donation = DonationService.link_donation(self.project, self.payment_transaction)
        self.assertIsNotNone(self.donation)
