import mock
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from django_facebook.utils import get_user_model
from revolv.base.models import RevolvUserProfile
from revolv.base.signals import create_profile_of_user
from revolv.payments.models import PaymentInstrumentType
from revolv.payments.services import PaymentService, PaymentServiceException
from revolv.project.models import Project


class PaymentServiceTest(TestCase):

    def setUp(self):
        post_save.disconnect(receiver=create_profile_of_user, sender=get_user_model())
        call_command('loaddata', 'user', 'revolvuserprofile', 'project')

    def tearDown(self):
        post_save.connect(create_profile_of_user, sender=get_user_model())

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
        project = Project.objects.get(id=1)
        user = RevolvUserProfile.objects.get(id=1)

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
        instrument_type = PaymentInstrumentType.objects.get(id=1)

        # Check that it returns True
        self.assertTrue(PaymentService.check_valid_payment_instrument(instrument_type))

    def test_check_valid_amount(self):
        """Verify that the amount is valid."""
        self.assertTrue(PaymentService.check_valid_amount(10.00))
        self.assertFalse(PaymentService.check_valid_amount(-10.00))
        self.assertFalse(PaymentService.check_valid_amount("abc"))
