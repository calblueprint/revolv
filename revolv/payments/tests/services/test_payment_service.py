import mock
from django.contrib.auth.models import User
from django.test import TestCase
from revolv.payments.models import PaymentInstrumentType
from revolv.payments.services import PaymentService, PaymentServiceException
from revolv.project.tests import CreateTestProjectMixin


class PaymentServiceTest(TestCase, CreateTestProjectMixin):

    @mock.patch('revolv.payments.services.PaymentService.check_valid_amount')
    @mock.patch('revolv.payments.services.PaymentService.check_valid_payment_instrument')
    def test_create_payment(self, mock_amount, mock_instrument):
        """Verify that we can create a payment."""
        # Force the amount to be valid
        mock_amount.return_value = True
        mock_instrument.return_value = True

        # Mock out a payment instrument with paypal by default
        instrument_type = mock.PropertyMock(
            return_value=PaymentInstrumentType.objects.get_paypal(),
        )
        payment_instrument = mock.Mock()
        type(payment_instrument).type = instrument_type
        project = self.create_test_project()
        user = (User.objects.create_user(username="john", password="doe")).revolvuserprofile

        # Make the payment
        PaymentService.create_payment(
            user,
            user,
            10.00,
            project,
            payment_instrument,
        )

        # Check that the charge was actually made
        payment_instrument.charge.assert_called_once()

        with self.assertRaises(PaymentServiceException):
            PaymentService.create_payment(
                user,
                None,
                10.00,
                project,
                payment_instrument,
            )

    def test_check_valid_payment_instrument(self):
        """Verify that we can get a valid payment instrument type."""
        # Mock out a payment instrument
        instrument_type = PaymentInstrumentType.objects.get_paypal()

        # Check that it returns True
        self.assertTrue(PaymentService.check_valid_payment_instrument(instrument_type))

    def test_check_valid_amount(self):
        """Verify that the amount is valid."""
        self.assertTrue(PaymentService.check_valid_amount(10.00))
        self.assertFalse(PaymentService.check_valid_amount(-10.00))
        self.assertFalse(PaymentService.check_valid_amount("abc"))
