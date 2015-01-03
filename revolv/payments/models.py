from django.contrib.auth.models import User
from django.db import models
from revolv.project.models import Project

INSTRUMENT_PAYPAL = 'paypal'
INSTRUMENT_CHECK = 'check'
INSTRUMENT_REINVEST = 'reinvest'


class PaymentInstrumentTypeManager(models.Manager):
    def get_paypal(self, queryset=None):
        """Return the PaymentInstrumentTypeManager for paypal payments."""
        if queryset is None:
            queryset = super(PaymentInstrumentTypeManager, self).get_queryset()
        return queryset.get(name="paypal")


class PaymentInstrumentType(models.Model):
    """
        Abstraction for a payment instrument. (e.g. Paypal)
    """
    name = models.CharField(max_length=80, unique=True)

    objects = PaymentInstrumentTypeManager()


class PaymentTransactionManager(models.Manager):
    def total_distinct_donors(self, queryset=None):
        """
        :return: The total number of donors that have ever donated to a RE-volv
            project. Useful for displaying stats on the homepage.
        """
        if queryset is None:
            queryset = super(PaymentTransactionManager, self).get_queryset()
        num_users = queryset.values("user").distinct().count()
        return num_users


class PaymentTransaction(models.Model):
    """
        Abstraction indicating one particular payment.
    """
    payment_instrument_type = models.ForeignKey(PaymentInstrumentType)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    amount = models.FloatField()

    objects = PaymentTransactionManager()


class DonationManager(models.Manager):
    """
        Simple manager for the donations model
    """

    def user_donations(self, user, queryset=None):
        """
        :return: Donations made by this user
        """
        if queryset is None:
            queryset = super(DonationManager, self).get_queryset()
        donations = queryset.filter(payment_transaction__user=user).order_by('created_at')
        return donations


class Donation(models.Model):
    """
        Abstraction of a donation from a user.
    """
    objects = DonationManager()

    payment_transaction = models.ForeignKey(PaymentTransaction)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project)

    def amount(self):
        """
        :return: The amount tied to this donation
        """
        return self.payment_transaction.amount

    def donor(self):
        """
        :return: The user tied to this donation
        """
        return self.payment_transaction.user
