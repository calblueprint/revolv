from __future__ import absolute_import

from collections import namedtuple
from math import floor

from paypalrestsdk import Payment
from revolv.payments.models import PaymentType


# Exceptions
class InvalidCreditCardException(Exception):
    pass


# Instruments
class PaymentInstrument(object):

    type = None

    def charge(self, amount):
        """
        Performs the necessary financial transactions to deem this method call an actual 'charge'.

        :param amount:
        """
        raise NotImplementedError('Cannot charge an unimplemented payment instrument.')


AbstractCreditCard = namedtuple(
    'AbstractCreditCard',
    ['type', 'number', 'expire_month', 'expire_year', 'cvv2', 'first_name', 'last_name'],
)


class CreditCard(AbstractCreditCard):

    def to_dict(self):
        """
        Return a dict formatted for Paypal consumption.
        :return: a dict
        """
        return {
            'type': self.type,
            'number': self.number,
            'expire_month': self.expire_month,
            'expire_year': self.expire_year,
            'cvv2': self.cvv2,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }


class PayPalCreditCardInstrument(PaymentInstrument):

    type = PaymentType.objects.get_paypal()

    def __init__(self, credit_card):
        if not isinstance(credit_card, CreditCard):
            raise InvalidCreditCardException('Tried to instatiate with an invalid credit card object.')
        self.credit_card = credit_card

    def charge(self, amount):
        """
        Documentation: https://github.com/paypal/PayPal-Python-SDK

        Charge the credit card for the given amount, floored to 2 decimal
        places. Raises InvalidCreditCardException if charge fails.

        Charing is enabled by default in settings.py. However, in development,
        charges go to the PayPal Sandbox, which means that your card shouldn't
        actually be charged (it'll just show up in the Sandbox charge history).
        When on production, payments go to a live PayPal, where cards are
        actually charged.

        :param amount:
        """
        amount = "{0:.2f}".format(floor(amount * 100) / 100.0)  # floor
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": self.credit_card.to_dict()
                }]
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Donation",
                        "sku": "item",
                        "price": amount,
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "This is a charitable donation to a Revolv funded project.",
            }]
        })

        if not payment.create():
            raise InvalidCreditCardException(payment.error)
        # Otherwise we're good
