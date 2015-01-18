from revolv.base.models import RevolvUserProfile
from revolv.payments.models import (INSTRUMENT_PAYPAL, INSTRUMENT_REPAYMENT,
                                    Payment, PaymentInstrumentType)
from revolv.settings import CHARGE_INSTRUMENT


# Exceptions


class PaymentServiceException(Exception):
    pass


# Services
class PaymentService(object):

    @classmethod
    def create_payment(cls, user, entrant, amount, project, payment_instrument):
        """
        Create a payment based on a configured payment_instrument.

        :user: a User making the payment
        :entrant: a User entering the payment
        :amount: float amount in USD
        :project: Project associated with payment
        :payment_instrument: a PaymentInstrument object (see PayPalCreditCardInstrument)
        :return: revolv.payments.models.PaymentTransaction
        """
        if not cls.check_valid_payment_instrument(payment_instrument.type):
            raise PaymentServiceException('Not a valid payment instrument.')
        if not cls.check_valid_amount(amount):
            raise PaymentServiceException('Not a valid dollar amount.')
        if not cls.check_valid_user_entrant(user, entrant, payment_instrument.type):
            raise PaymentServiceException('Improper Payment structure. Invalid entrant or user.')

        if CHARGE_INSTRUMENT:
            payment_instrument.charge(amount)
        payment = Payment(
            user=user,
            entrant=entrant,
            amount=float(amount),
            project=project,
            payment_instrument_type=payment_instrument.type
        )
        payment.save()
        return payment

    @classmethod
    def check_valid_payment_instrument(cls, payment_instrument_type):
        """Return True if the payment instrument type is legit."""
        return (
            isinstance(payment_instrument_type, PaymentInstrumentType) and
            PaymentInstrumentType.objects.get(
                name=payment_instrument_type.name)
        )

    @classmethod
    def check_valid_amount(cls, amount):
        """Return True if the amount is greater than zero."""
        try:
            amount = float(amount)
            return amount > 0.0
        except ValueError:
            return False

    @classmethod
    def check_valid_user_entrant(cls, user, entrant, payment_instrument_type):
        if not isinstance(entrant, RevolvUserProfile):
            return False
        if payment_instrument_type.name == INSTRUMENT_PAYPAL and user != entrant:
            return False
        if payment_instrument_type.name == INSTRUMENT_REPAYMENT and isinstance(user, RevolvUserProfile):
            return False
        return True
