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
        Abstraction for a payment instrument. A payment instrument is defined as
        anything that can be used to create a payment (for example, paypal or any
        other payment service). Types of payment that the RE-volv app currently
        supports are as follows:

        1. "paypal": a payment that was made via a credit card processed through
           the paypal REST sdk. TODO: the distinction between an actual payment
           through a paypal account and a payment made with credit card but processed
           by paypal.
        2. "check": a record or a payment that was made directly to a RE-volv
           administrator via paper check. These must be entered into the app via
           the UI in the administrator dashboard page in order for our database to
           know about them.
        3. "repayment" (DEPRECATED): this represents a payment that was made from a
           community organization that RE-volv has already funded and is a return on
           that solar panel investment. These are available to be reinvested.
        4. "reinvestment": this is a payment that was allocated to a new project as
           part the revolving funding model - the money originally came from an organic
           donation to an already completed project, and then the community repayed
           revolv the money that is represented in the Payment that has this PaymentInstrumentType.
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


# class PaymentFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = "revolv.payments.Payment"

#     user = factory.SubFactory("revolv.base.models.RevolvUserProfileFactory")
#     entrant = factory.SubFactory("revolv.base.models.RevolvUserProfileFactory")
#     amount = 20.00
#     project = factory.SubFactory("revolv.project.models.ProjectFactory")
#     payment_instrument_type = PaymentInstrumentType.objects.get_paypal()
#     created_at = datetime.datetime.now()


# class PaymentFactories(object):
#     base = PaymentFactory


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
    # factories = PaymentFactories
