import mock
from django.test import TestCase
from revolv.payments.forms import CreditCardDonationForm


class CreditCardDonationFormTestCase(TestCase):

    def test_valid_form(self):
        """Verify that a valid form is valid."""
        cc_form = CreditCardDonationForm({
            'type': 'visa',
            'first_name': 'William',
            'last_name': 'Taft',
            'expire_month': '06',
            'expire_year': '14',
            'cvv2': '00',
            'number': '1234123412341234',
            'amount': '10.00',
        })
        self.assertTrue(cc_form.is_valid())

    @mock.patch('revolv.payments.forms.PaymentService')
    def test_form_process_payment(self, mock_payment_service):
        """Verify that we can process a payment with the form."""
        # Setup mocks
        mock_pt = mock.Mock()
        mock_payment_service.create_payment.return_value = mock_pt

        cc_form = CreditCardDonationForm({
            'type': 'visa',
            'first_name': 'William',
            'last_name': 'Taft',
            'expire_month': '06',
            'expire_year': '14',
            'cvv2': '00',
            'number': '1234123412341234',
            'amount': '10.00',
        })

        # Test the payment
        mock_project = mock.Mock()
        self.assertEquals(
            mock_pt,
            cc_form.process_payment(mock_project, mock_pt)
        )

        self.assertTrue(mock_payment_service.create_payment.called)
