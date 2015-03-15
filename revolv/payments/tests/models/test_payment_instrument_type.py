from django.test import TestCase
from revolv.payments.models import (PAYTYPE_CHECK, PAYTYPE_PAYPAL,
                                    PAYTYPE_REINVESTMENT, PaymentType)


class PaymentTypeTest(TestCase):

    def test_get_payment_types(self):
        self.assertEqual(4, len(PaymentType.objects.all()))
        self.assertEqual(PAYTYPE_PAYPAL, PaymentType.objects.first().name)
        self.assertEqual(PAYTYPE_REINVESTMENT, PaymentType.objects.get(id=2).name)
        self.assertEqual(PAYTYPE_CHECK, PaymentType.objects.get(id=3).name)
