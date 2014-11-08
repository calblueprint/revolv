from django.contrib.auth.models import User
from django.db import models
from revolv.project.models import Project

INSTRUMENT_PAYPAL = 'paypal'
INSTRUMENT_CHECK = 'check'


class PaymentInstrumentType(models.Model):
    """
        Abstraction for a payment instrument. (e.g. Paypal)
    """
    name = models.CharField(max_length=80, unique=True)


class PaymentTransaction(models.Model):
    """
        Abstraction indicating one particular payment.
    """
    payment_instrument_type = models.ForeignKey(PaymentInstrumentType)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    amount = models.FloatField()


class DonationManager(models.Manager):
    """
        Simple manager for the donations model
    """

    def donated_projects(self, user, queryset=None):
        """
        :return: Projects to which this user has donated
        """
        if queryset is None:
            return self.user_donations(user).value_list('project', flat=True)
        return queryset.value_list('project', flat=True)

    def user_donations(self, user, queryset=None):
        """
        :return: Donations made by this user
        """
        if queryset is None:
            queryset = super(DonationManager, self).get_queryset()
        donations = queryset.filter(donor=user).order_by('created_at')
        return donations


class Donation(models.Model):
    """
        Abstraction of a donation from a user.
    """
    objects = DonationManager()

    payment_transaction = models.ForeignKey(PaymentTransaction)
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project)

    @property
    def amount(self):
        """
        :return: The amount tied to this donation
        """
        return self.payment_transaction.amount

    @property
    def donor(self):
        """
        :return: The user tied to this donation
        """
        return self.payment_transaction.user
