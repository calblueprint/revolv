from django.db import models
from revolv.base.models import RevolvUserProfile
from revolv.lib.utils import ImportProxy

PAYTYPE_PAYPAL = 'paypal'
PAYTYPE_CHECK = 'check'
PAYTYPE_REINVESTMENT = 'reinvestment'


class AdminRepaymentManager(models.Manager):
    def repayments(self, admin=None, project=None, queryset=None):
        """
        :return: AdminRepayments associated with this admin and project
        """
        if queryset is None:
            queryset = super(AdminRepaymentManager, self).get_queryset()
        if admin:
            queryset = queryset.filter(admin=admin).order_by('created_at')
        if project:
            queryset = queryset.filter(project=project).order_by('created_at')
        return queryset


class AdminRepayment(models.Model):
    """
    Repayment from completed project.
    TODO: more documentation
    """
    amount = models.FloatField()
    admin = models.ForeignKey(RevolvUserProfile)
    project = models.ForeignKey("project.Project")

    created_at = models.DateTimeField(auto_now_add=True)

    objects = AdminRepaymentManager()
    factories = ImportProxy("revolv.payments.factories", "AdminRepaymentFactories")


class AdminReinvestmentManager(models.Manager):
    def reinvestments(self, admin=None, project=None, queryset=None):
        """
        :return: AdminReinvestment associated with this admin and project
        """
        if queryset is None:
            queryset = super(AdminReinvestmentManager, self).get_queryset()
        if admin:
            queryset = queryset.filter(admin=admin).order_by('created_at')
        if project:
            queryset = queryset.filter(project=project).order_by('created_at')
        return queryset


class AdminReinvestment(models.Model):
    """
    Reinvestment for ongoing project.
    TODO: more documentation
    """
    amount = models.FloatField()
    admin = models.ForeignKey(RevolvUserProfile)
    project = models.ForeignKey("project.Project")

    created_at = models.DateTimeField(auto_now_add=True)

    objects = AdminReinvestmentManager()
    factories = ImportProxy("revolv.payments.factories", "AdminReinvestmentFactories")


class PaymentTypeManager(models.Manager):
    def get_paypal(self, queryset=None):
        """Return the PaymentTypeManager for paypal payments."""
        if queryset is None:
            queryset = super(PaymentTypeManager, self).get_queryset()
        return queryset.get(name=PAYTYPE_PAYPAL)

    def get_reinvestment(self, queryset=None):
        """Return the PaymentTypeManager for reinvestment payments."""
        if queryset is None:
            queryset = super(PaymentTypeManager, self).get_queryset()
        return queryset.get(name=PAYTYPE_REINVESTMENT)


class PaymentType(models.Model):
    """
    Abstraction for a payment. A payment type is defined as anything that can
    be used to create a payment (for example, Paypal, check, or any other
    payment service). Types of payment that the RE-volv app currently supports
    are as follows:

    1. "paypal": a payment that was made via a credit card processed through
        the paypal REST sdk. TODO: the distinction between an actual payment
        through a paypal account and a payment made with credit card but
        processed by paypal.
    2. "check": a record or a payment that was made directly to a RE-volv
        administrator via paper check. These must be entered into the app via
        the UI in the administrator dashboard page in order for our database to
        know about them.
    3. "reinvestment": this is a payment that was allocated to a new project as
        part the revolving funding model - the money originally came from an
        organic donation to an already completed project, and then the
        community repayed RE-volv the money that is represented in the Payment
        that has this PaymentType.
    """
    name = models.CharField(max_length=80, unique=True)

    objects = PaymentTypeManager()


class RepaymentManager(models.Manager):
    def repayments(self, **kwargs):
        if kwargs.get('queryset') is None:
            queryset = super(RepaymentManager, self).get_queryset()
        if kwargs.get('user'):
            queryset = queryset.filter(user=kwargs['user']).order_by('created_at')
        if kwargs.get('project'):
            queryset = queryset.filter(project=kwargs['project']).order_by('created_at')
        if kwargs.get('admin_repayment'):
            queryset = queryset.filter(admin_repayment=kwargs['admin_repayment']).order_by('created_at')
        return queryset


class Repayment(models.Model):
    """
    Abstraction for a repayment.
    """
    user = models.ForeignKey(RevolvUserProfile)
    project = models.ForeignKey("project.Project")
    admin_repayment = models.ForeignKey(AdminRepayment)

    amount = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    objects = RepaymentManager()
    factories = ImportProxy("revolv.payments.factories", "RepaymentFactories")


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
        return self.payments(user, project, queryset).exclude(payment_type__name=PAYTYPE_REINVESTMENT)

    def reinvestments(self, user=None, project=None, queryset=None):
        """
        :return: Returns all reinvestment payments that are associated with
                 this user.
        """
        return self.payments(user, project, queryset).filter(payment_type__name=PAYTYPE_REINVESTMENT)

    def repayments(self, user, admin=None, project=None, queryset=None):
        """
        :return: Returns all the repayments that are associated with this
                 user.
        """
        return AdminRepayment.objects.filter(revolvuserprofiles__in=user, projects__in=project).distinct()

    def total_distinct_organic_donors(self, queryset=None):
        """
        :return: The total number of organic donors that have ever donated to a
            RE-volv project. Useful for displaying stats on the homepage.
        """
        if queryset is None:
            queryset = self.donations()
        num_users = queryset.values("user").distinct().count()
        return num_users


class Payment(models.Model):
    """
    Abstraction indicating one particular payment.
    """
    user = models.ForeignKey(RevolvUserProfile)
    project = models.ForeignKey("project.Project")

    entrant = models.ForeignKey(RevolvUserProfile, related_name='entrant')
    payment_type = models.ForeignKey(PaymentType)
    created_at = models.DateTimeField(auto_now_add=True)

    admin_reinvestment = models.ForeignKey(AdminReinvestment, blank=True, null=True)

    amount = models.FloatField()

    objects = PaymentManager()
    factories = ImportProxy("revolv.payments.factories", "PaymentFactories")
