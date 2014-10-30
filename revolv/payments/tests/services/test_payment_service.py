import mock
from django.contrib.auth.models import User
from django.test import TestCase
from revolv.payments.models import PaymentInstrumentType
from revolv.payments.services import PaymentService


class PaymentServiceTest(TestCase):

    fixtures = ['supported_instruments.json']

    def setUp(self):
        self.user = User(username='billnye')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    @mock.patch('revolv.payments.services.PaymentService.check_valid_amount')
    @mock.patch('revolv.payments.services.PaymentService.check_valid_payment_instrument')
    def test_create_payment(self, mock_amount, mock_instrument):
        """Verify that we can create a payment."""
        # Force the amount to be valid
        mock_amount.return_value = True
        mock_instrument.return_value = True

        # Mock out a payment instrument
        instrument_type = mock.PropertyMock(
            return_value=PaymentInstrumentType.objects.get(id=1),
        )
        payment_instrument = mock.Mock()
        type(payment_instrument).type = instrument_type

        # Make the payment
        PaymentService.create_payment(
            self.user,
            10.00,
            payment_instrument,
        )

        # Check that the charge was actually made
        payment_instrument.charge.assert_called_once()

    def test_check_valid_payment_instrument(self):
        """Verify that we can get a valid payment instrument type."""
        # Mock out a payment instrument
        instrument_type = PaymentInstrumentType.objects.get(id=1)

        # Check that it returns True
        self.assertTrue(PaymentService.check_valid_payment_instrument(instrument_type))

    def test_check_valid_amount(self):
        """Verify that the amount is valid."""
        self.assertTrue(PaymentService.check_valid_amount(10.00))
        self.assertFalse(PaymentService.check_valid_amount(-10.00))
        self.assertFalse(PaymentService.check_valid_amount("abc"))
