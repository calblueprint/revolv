from django.test import TestCase
from revolv.payments.models import INSTRUMENT_PAYPAL, PaymentInstrumentType


class PaymentInstrumentTypeTest(TestCase):

    fixtures = ['supported_instruments.json']

    def test_get_payment_instrument_types(self):

        self.assertEqual(1, len(PaymentInstrumentType.objects.all()))
        self.assertEqual(INSTRUMENT_PAYPAL, PaymentInstrumentType.objects.first().name)
