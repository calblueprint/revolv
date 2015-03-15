from revolv.base.models import RevolvUserProfile
from revolv.payments.models import PAYTYPE_PAYPAL, Payment, PaymentType
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
        :entrant: a User entering the payment. if user==entrant then organic payment.
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
            payment_type=payment_instrument.type
        )
        payment.save()
        return payment

    @classmethod
    def create_repayment(cls, entrant, amount, project):
        donations = Payment.objects.all_donations().filter(project=project)
        total = project.amount_donated
        for donation in donations:
            repayment = Payment(
                user=donation.user,
                entrant=entrant,
                amount=float(amount) * (donation.amount / total),
                project=project,
                payment_type=PaymentType.objects.get_repayment()
            )
            repayment.save()
        return

    @classmethod
    def create_check(cls, user, entrant, amount, project):
        check = Payment(
            user=user,
            entrant=entrant,
            amount=float(amount),
            project=project,
            payment_type=PaymentType.objects.get_check()
        )
        check.save()
        return check

    @classmethod
    def check_valid_payment_instrument(cls, payment_type):
        """Return True if the payment instrument type is legit."""
        return (
            isinstance(payment_type, PaymentType) and
            PaymentType.objects.get(
                name=payment_type.name)
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
    def check_valid_user_entrant(cls, user, entrant, payment_type):
        if not isinstance(entrant, RevolvUserProfile):
            return False
        if not isinstance(user, RevolvUserProfile):
            return False
        if payment_type.name == PAYTYPE_PAYPAL and user != entrant:
            return False
        return True
