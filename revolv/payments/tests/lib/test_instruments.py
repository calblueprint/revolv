from django.test import TestCase

from revolv.payments.lib.instruments import (
    CreditCard,
    PayPalCreditCardInstrument,
    InvalidCreditCardException,
)


class CreditCardTestCase(TestCase):

    def test_create_credit_card(self):
        """Verify that we can create a credit card."""
        CreditCard('visa', '1234123412341234', '01', '2018', '000', 'John', 'Smith')

    def test_check_cannot_change_credit_card(self):
        """Verify that we cannot change the credit card once manipulated."""
        c = CreditCard('visa', '1234123412341234', '01', '2018', '000', 'John', 'Smith')
        with self.assertRaises(AttributeError):
            c.expire_year = 2

    def test_check_converts_to_dict(self):
        """Verify that the credit card converts to dict."""
        c = CreditCard('visa', '1234123412341234', '01', '2018', '000', 'John', 'Smith')
        self.assertIsNotNone(c.to_dict())


class PayPalCreditCardInstrumentTestCase(TestCase):

    def setUp(self):
        self.credit_card = CreditCard('visa', '4032038705456659', '10', '2019', '000', 'John', 'Smith')

    def test_create_payment_instrument(self):
        """Verify that we can create the payment instrument."""
        # Check regular way works
        self.assertIsNotNone(PayPalCreditCardInstrument(self.credit_card))

        # Check that it throws an error
        with self.assertRaises(InvalidCreditCardException):
            PayPalCreditCardInstrument(None)

    def test_charge_payment_instrument(self):
        """Verify that we can charge the credit card via PayPal."""
        instrument = PayPalCreditCardInstrument(self.credit_card)
        instrument.charge(1.00)