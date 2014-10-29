from revolv.payments.models import (Donation, PaymentInstrumentType,
                                    PaymentTransaction)


# Exceptions


class PaymentServiceException(Exception):
    pass


# Services
class PaymentService(object):

    @classmethod
    def create_payment(cls, user, amount, payment_instrument):
        """Create a payment based on a configured payment_instrument."""
        # TODO(anthonys): document args
        if not cls.check_valid_payment_instrument(payment_instrument.type):
            raise PaymentServiceException('Not a valid payment instrument.')
        if not cls.check_valid_amount(amount):
            raise PaymentServiceException('Not a valid dollar amount.')

        payment_instrument.charge(amount)
        payment_transaction = PaymentTransaction(
            user=user,
            amount=float(amount),
            payment_instrument_type=payment_instrument.type,
        )
        payment_transaction.save()
        return payment_transaction

    @classmethod
    def check_valid_payment_instrument(cls, payment_instrument_type):
        """Return True if the payment instrument type is legit."""
        return (
            isinstance(payment_instrument_type, PaymentInstrumentType) and
            PaymentInstrumentType.objects.get(name=payment_instrument_type.name)
        )

    @classmethod
    def check_valid_amount(cls, amount):
        """Return True if the amount is greater than zero."""
        try:
            amount = float(amount)
            return amount > 0.0
        except:
            return False
