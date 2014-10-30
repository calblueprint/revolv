from django.contrib.auth.models import User
from django.test import TestCase
from revolv.payments.models import PaymentInstrumentType, PaymentTransaction


class PaymentTransactionTest(TestCase):

    def test_payment_create(self):
        """Verify that the payment transaction can be created."""
        user = User(username='user1')
        instrument_type = PaymentInstrumentType(name='test instrument')

        pt = PaymentTransaction(amount=10.00, user=user, payment_instrument_type=instrument_type)
