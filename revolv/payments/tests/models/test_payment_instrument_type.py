from django.test import TestCase
from revolv.payments.models import (INSTRUMENT_CHECK, INSTRUMENT_PAYPAL,
                                    INSTRUMENT_REINVESTMENT,
                                    INSTRUMENT_REPAYMENT,
                                    PaymentInstrumentType)


class PaymentInstrumentTypeTest(TestCase):

    def test_get_payment_instrument_types(self):

        self.assertEqual(4, len(PaymentInstrumentType.objects.all()))
        self.assertEqual(INSTRUMENT_PAYPAL, PaymentInstrumentType.objects.first().name)
        self.assertEqual(INSTRUMENT_REINVESTMENT, PaymentInstrumentType.objects.get(id=2).name)
        self.assertEqual(INSTRUMENT_CHECK, PaymentInstrumentType.objects.get(id=3).name)
        self.assertEqual(INSTRUMENT_REPAYMENT, PaymentInstrumentType.objects.get(id=4).name)
