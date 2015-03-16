from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from revolv.base.models import RevolvUserProfile
from revolv.lib.utils import ImportProxy

PAYTYPE_PAYPAL = 'paypal'
PAYTYPE_CHECK = 'check'
PAYTYPE_REINVESTMENT = 'reinvestment'


class NotEnoughFundingException(Exception):
    pass


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
    linked_to_users = models.BooleanField(default=False)

    objects = AdminRepaymentManager()
    factories = ImportProxy("revolv.payments.factories", "AdminRepaymentFactories")


@receiver(signals.post_save, sender=AdminRepayment)
def postSaveAdminRepayment(**kwargs):
    """
    When an AdminRepayment is saved, a Repayment is generated for all donors
    to a project.
    """
    instance = kwargs.get('instance')
    for donor in instance.project.donors.all():
        repayment = Repayment(user=donor,
                              project=instance.project,
                              admin_repayment=instance,
                              amount=(instance.project.proportion_donated(donor) * instance.amount),
                              )
        repayment.save()


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

    test_obj = models.BooleanField(default=False)

    objects = AdminReinvestmentManager()
    factories = ImportProxy("revolv.payments.factories", "AdminReinvestmentFactories")


@receiver(signals.pre_init, sender=AdminReinvestment)
def preInitAdminReinvestment(**kwargs):
    """
    Raises a NotEnoughFundingException if there is not enough money to reinvest
    """
    init_kwargs = kwargs.get('kwargs')
    if not init_kwargs:
        raise NotEnoughFundingException()
    if init_kwargs.get('test_obj'):
        return
    invest_amount = init_kwargs.get('amount') or 0.0

    global_repay_amount = AdminRepayment.objects.aggregate(
        models.Sum('amount')
    )['amount__sum'] or 0.0
    global_reinvest_amount = AdminReinvestment.objects.aggregate(
        models.Sum('amount')
    )['amount__sum'] or 0.0
    global_reinvest_pool = global_repay_amount - global_reinvest_amount
    if global_reinvest_pool - invest_amount < 0.0:
        raise NotEnoughFundingException()


@receiver(signals.post_save, sender=AdminReinvestment)
def postSaveAdminReinvestment(**kwargs):
    """
    When an AdminReinvestment is saved, we pool as many donors as we need to
    fund the reinvestment

    !!! TODO: prioritize users by preference
    """
    instance = kwargs.get('instance')
    if instance.test_obj:
        return
    total_left = instance.amount
    pending_reinvestors = []
    for user in RevolvUserProfile.objects.filter(reinvest_pool__gt=0.0):
        total_left -= user.reinvest_pool
        reinvest_amount = user.reinvest_pool + min(0.0, total_left)
        pending_reinvestors.append((user, reinvest_amount))
        if total_left <= 0.0:
            break
    for (user, amount) in pending_reinvestors:
        reinvestment = Payment(user=user,
                               project=instance.project,
                               entrant=instance.admin,
                               payment_type=PaymentType.objects.get_reinvestment(),
                               admin_reinvestment=instance,
                               amount=amount
                               )
        reinvestment.save()


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


@receiver(signals.post_save, sender=Repayment)
def postSaveRepayment(**kwargs):
    """
    When a Repayment is saved, we increment the reinvest_pool in the related
    user
    """
    instance = kwargs.get('instance')
    instance.user.reinvest_pool += instance.amount
    instance.user.save()


@receiver(signals.pre_delete, sender=Repayment)
def preDeleteRepayment(**kwargs):
    """
    Before a Repayment is deleted, we decrement the reinvest_pool in the related
    user
    """
    instance = kwargs.get('instance')
    instance.user.reinvest_pool -= instance.amount
    instance.user.save()


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


@receiver(signals.post_save, sender=Payment)
def postSavePayment(**kwargs):
    """
    When a Payment is saved, if it is a reinvestment, we decrement the
    reinvest_pool in the related user
    """
    instance = kwargs.get('instance')
    if instance.payment_type == PaymentType.objects.get_paypal():
        instance.project.donors.add(instance.user)
    elif instance.payment_type == PaymentType.objects.get_reinvestment():
        instance.user.reinvest_pool -= instance.amount
        instance.user.save()


@receiver(signals.pre_delete, sender=Payment)
def preDeletePayment(**kwargs):
    """
    Before a Payment is deleted, if it is a reinvestment, we increment the
    reinvest_pool in the related user
    """
    instance = kwargs.get('instance')
    if instance.payment_type == PaymentType.objects.get_paypal():
        instance.project.donors.remove(instance.user)
    elif instance.payment_type == PaymentType.objects.get_reinvestment():
        instance.user.reinvest_pool += instance.amount
        instance.user.save()
