from django.test import TestCase
from revolv.payments.models import PaymentType


class PaymentTypeTest(TestCase):
    def test_get_payment_types(self):
        self.assertEqual(3, len(PaymentType.objects.all()))
        self.assertEqual(PaymentType._PAYPAL, PaymentType.objects.first().name)
        self.assertEqual(PaymentType._REINVESTMENT, PaymentType.objects.get(id=1).name)
        self.assertEqual(PaymentType._CHECK, PaymentType.objects.get(id=2).name)
