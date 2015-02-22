from django.db import models
from revolv.base.models import RevolvUserProfile

INSTRUMENT_PAYPAL = 'paypal'
INSTRUMENT_CHECK = 'check'
INSTRUMENT_REINVESTMENT = 'reinvestment'
INSTRUMENT_REPAYMENT = 'repayment'


class PaymentInstrumentTypeManager(models.Manager):
    def get_paypal(self, queryset=None):
        """Return the PaymentInstrumentTypeManager for paypal payments."""
        if queryset is None:
            queryset = super(PaymentInstrumentTypeManager, self).get_queryset()
        return queryset.get(name=INSTRUMENT_PAYPAL)

    def get_reinvestment(self, queryset=None):
        """Return the PaymentInstrumentTypeManager for reinvestment payments."""
        if queryset is None:
            queryset = super(PaymentInstrumentTypeManager, self).get_queryset()
        return queryset.get(name=INSTRUMENT_REINVESTMENT)

    def get_repayment(self, queryset=None):
        """Return the PaymentInstrumentTypeManager for repayments."""
        if queryset is None:
            queryset = super(PaymentInstrumentTypeManager, self).get_queryset()
        return queryset.get(name=INSTRUMENT_REPAYMENT)


class PaymentInstrumentType(models.Model):
    """
        Abstraction for a payment instrument. (e.g. Paypal)
    """
    name = models.CharField(max_length=80, unique=True)

    objects = PaymentInstrumentTypeManager()


class PaymentManager(models.Manager):
    """
        Simple manager for the Payment model.
    """

    def payments(self, user=None, project=None, queryset=None):
        """
        :return: Payments associated with this user and project
        """
        if queryset is None:
            queryset = super(PaymentManager, self).get_queryset()
        if user:
            queryset = queryset.filter(user=user).order_by('created_at')
        if project:
            queryset = queryset.filter(project=project).order_by('created_at')
        return queryset

    def donations(self, user=None, project=None, queryset=None):
        """
        :return: Returns all payments that are not repayments or reinvestments
                 associated with this user.
        """
        return self.payments(user, project, queryset).exclude(payment_instrument_type__name=INSTRUMENT_REINVESTMENT).exclude(payment_instrument_type__name=INSTRUMENT_REPAYMENT)

    def reinvestments(self, user=None, project=None, queryset=None):
        """
        :return: Returns all reinvestment payments that are associated with
                 this user.
        """
        return self.payments(user, project, queryset).filter(payment_instrument_type__name=INSTRUMENT_REINVESTMENT)

    def repayments(self, user=None, project=None, queryset=None):
        """
        :return: Returns all the repayments that are associated with this
                 user.
        """
        return self.payments(user, project, queryset).filter(payment_instrument_type__name=INSTRUMENT_REPAYMENT)

    def all_donations(self, queryset=None):
        """
        :return: Returns all the donations made on the application. Useful helper for distinct
                 donors.
        """
        return self.payments(queryset=queryset).exclude(payment_instrument_type__name=INSTRUMENT_REINVESTMENT).exclude(payment_instrument_type__name=INSTRUMENT_REPAYMENT)

    def total_distinct_donors(self, queryset=None):
        """
        :return: The total number of donors that have ever donated to a RE-volv
            project. Useful for displaying stats on the homepage.
        """
        if queryset is None:
            queryset = self.all_donations()
        num_users = queryset.values("user").distinct().count()
        return num_users


class Payment(models.Model):
    """
        Abstraction indicating one particular payment.
    """
    user = models.ForeignKey(RevolvUserProfile)
    entrant = models.ForeignKey(RevolvUserProfile, related_name='entrant')
    amount = models.FloatField()
    project = models.ForeignKey("project.Project")
    payment_instrument_type = models.ForeignKey(PaymentInstrumentType)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PaymentManager()
