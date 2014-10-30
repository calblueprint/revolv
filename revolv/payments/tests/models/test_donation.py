from django.contrib.auth.models import User
from django.test import TestCase
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
