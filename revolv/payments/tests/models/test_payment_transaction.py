from django.contrib.auth.models import User
from django.test import TestCase
from revolv.payments.models import PaymentInstrumentType, PaymentTransaction


class PaymentTransactionTest(TestCase):

    def test_payment_create(self):
        """Verify that the payment transaction can be created."""
        user = User(username='user1')
        instrument_type = PaymentInstrumentType(name='test instrument')

        PaymentTransaction(amount=10.00, user=user, payment_instrument_type=instrument_type)

    def test_total_distinct_donors(self):
        user1 = User.objects.create_user("user1")
        user2 = User.objects.create_user("user2")
        user3 = User.objects.create_user("user3")

        instrument_type = PaymentInstrumentType.objects.get_paypal()

        self.assertEquals(PaymentTransaction.objects.total_distinct_donors(), 0)
        PaymentTransaction.objects.create(amount=10.00, user=user1, payment_instrument_type=instrument_type)
        self.assertEquals(PaymentTransaction.objects.total_distinct_donors(), 1)
        PaymentTransaction.objects.create(amount=10.00, user=user1, payment_instrument_type=instrument_type)
        self.assertEquals(PaymentTransaction.objects.total_distinct_donors(), 1)
        PaymentTransaction.objects.create(amount=10.00, user=user2, payment_instrument_type=instrument_type)
        self.assertEquals(PaymentTransaction.objects.total_distinct_donors(), 2)
        PaymentTransaction.objects.create(amount=10.00, user=user3, payment_instrument_type=instrument_type)
        self.assertEquals(PaymentTransaction.objects.total_distinct_donors(), 3)
