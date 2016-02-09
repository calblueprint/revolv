from django.db import models
from django.contrib.auth.models import User

from revolv.lib.utils import ImportProxy

from datetime import date


class AdminRepaymentManager(models.Manager):
    """
    Manager for AdminRepayment.
    """

    def repayments(self, admin=None, project=None, queryset=None):
        """
        :return: AdminRepayments associated with this admin and project.
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
    Model representing a single, admin-controlled "contact point" for a
    repayment from a completed RE-volv project.

    When a RE-volv project makes a repayment, we create a representative
    AdminRepayment instance in our database. Creating an AdminRepayment
    automatically generates a RepaymentFragment for each RevolvUserProfile who
    organically donated to the project.  For user U, project P, and
    AdminRepayment R, the "amount" of the U's RepaymentFragment will be:

        ((U's donation to P) / (Total organic donations to P)) * R.amount

    Generating a RepaymentFragment for a user increases that user's pool of
    reinvestable money.

    We need a single "contact point" representing a repayment so that admins
    have the ability to "revoke" a repayment, if it was entered falsely.
    Deleting an AdminRepayment also deletes any RepaymentFragments associated
    with it, effectively erasing any trace of the repayment.

    ::Signals::
    pre_init
        Make sure that related project is indeed complete, else throw a
        ProjectNotCompleteException to disallow instantiation of an invalid
        AdminRepayment.
    post_save
        When an AdminRepayment is saved, a RepaymentFragment is generated for
        all donors to a project, each weighted by that donor's proportion of the
        contribution to the project.
    """
    amount = models.FloatField()
    admin = models.ForeignKey('base.RevolvUserProfile')
    project = models.ForeignKey("project.Project")

    created_at = models.DateTimeField(auto_now_add=True)

    objects = AdminRepaymentManager()
    factories = ImportProxy("revolv.payments.factories", "AdminRepaymentFactories")

    def __unicode__(self):
        return '%s for %s' % (self.amount, self.project)


class AdminReinvestmentManager(models.Manager):
    """
    Manager for AdminReinvestment.
    """

    def reinvestments(self, admin=None, project=None, queryset=None):
        """
        :return: AdminReinvestment associated with this admin and project.
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
    Model representing a single, admin-controlled "contact point" for a
    reinvestment into an ongoing RE-volv project.

    RE-volv usually only reinvests into a project at its launch, but it is still
    possible for an admin to put in a reinvestment at any time.

    Creating an AdminReinvestment automatically pools money from users with a
    non-zero pool of reinvestable money, prioritizing users that have a
    preference for the Category of the project being reinvested into. (A user's
    pool of reinvestable money consists of the sum of unspent repayment
    fragments to that user.)

    We generate a Payment of type 'reinvestment_fragment' for each user that we
    pooled money from with the amount of money that we pooled from that user,
    and also decrement that user's pool of reinvestable money.

    An AdminReinvestment cannot be created if there are insufficient funds.

    We need a single "contact point" representing a reinvestment so that admins
    have the ability to "revoke" a reinvestment, if it was entered falsely.
    Deleting an AdminReinvestment also deletes any "reinvestment_fragment"-type
    Payments associated with it, effectively erasing any trace of the
    reinvestment.

    ::Signals::
    pre_init
        Raises a NotEnoughFundingException before __init__ if there are not
        enough funds for this AdminReinvestment.
    post_save
        When an AdminReinvestment is saved, we pool as many donors as we need to
        fund the reinvestment, prioritizing users that have a preference for the
        Category of the project begin invested into. We only consider users that
        have a non-zero pool of investable money.
        !!! TODO: actually prioritize by Category
    """
    amount = models.FloatField()
    admin = models.ForeignKey('base.RevolvUserProfile')
    project = models.ForeignKey("project.Project")

    created_at = models.DateTimeField(auto_now_add=True)

    objects = AdminReinvestmentManager()
    factories = ImportProxy("revolv.payments.factories", "AdminReinvestmentFactories")

    def __unicode__(self):
        return '%s for %s' % (self.amount, self.project)


class PaymentTypeManager(models.Manager):
    """
    Manager for PaymentType.
    """

    def get_check(self, queryset=None):
        """Return the PaymentTypeManager for check payments."""
        if queryset is None:
            queryset = super(PaymentTypeManager, self).get_queryset()
        return queryset.get(name=PaymentType._CHECK)

    def get_paypal(self, queryset=None):
        """Return the PaymentTypeManager for paypal payments."""
        if queryset is None:
            queryset = super(PaymentTypeManager, self).get_queryset()
        return queryset.get(name=PaymentType._PAYPAL)

    def get_stripe(self, queryset=None):
        if queryset is None:
            queryset = super(PaymentTypeManager, self).get_queryset()
        return queryset.get(name=PaymentType._STRIPE)

    def get_reinvestment_fragment(self, queryset=None):
        """Return the PaymentTypeManager for reinvestment_fragment payments."""
        if queryset is None:
            queryset = super(PaymentTypeManager, self).get_queryset()
        return queryset.get(name=PaymentType._REINVESTMENT)


class PaymentType(models.Model):
    """
    Abstraction for a payment type. A payment type is defined as anything that
    can be used to create a payment (for example, Paypal, check, or any other
    payment service). Types of payment that the RE-volv app currently supports
    are as follows:

    'paypal'
        A payment that was made via a credit card processed through
        the paypal REST sdk.
        !!!TODO: the distinction between an actual payment through a paypal
        account and a payment made with credit card but processed by paypal.
    'check'
        A record or a payment that was made directly to a RE-volv
        administrator via paper check. These must be entered into the app via
        the UI in the administrator dashboard page in order for our database to
        know about them.
    'reinvestment_fragment'
        A fragment of a reinvestment that was allocated to a project as part the
        revolving funding model. The sum of all reinvestment_fragments for all
        donors to a particular project will equal the amount reinvested into
        that project. Reinvestment money originates from repayments made by
        already completed projects.
    """
    _PAYPAL = 'paypal'
    _STRIPE = 'stripe'
    _CHECK = 'check'
    _REINVESTMENT = 'reinvestment_fragment'

    name = models.CharField(max_length=80, unique=True)

    objects = PaymentTypeManager()

    @property
    def paypal(self):
        return self.objects.get_paypal()

    @property
    def stripe(self):
        return self.objects.get_stripe()

    @property
    def reinvestment_fragment(self):
        return self.objects.get_reinvestment_fragment()

    def __unicode__(self):
        return self.name


class RepaymentFragmentManager(models.Manager):
    """
    Manager for repayments.
    """

    def repayments(self, **kwargs):
        """
        :return:
            RepaymentFragments associated with this user, project, and/or
            AdminRepayment.
        """
        if kwargs.get('queryset') is None:
            queryset = super(RepaymentFragmentManager, self).get_queryset()
        if kwargs.get('user'):
            queryset = queryset.filter(user=kwargs['user']).order_by('created_at')
        if kwargs.get('project'):
            queryset = queryset.filter(project=kwargs['project']).order_by('created_at')
        if kwargs.get('admin_repayment'):
            queryset = queryset.filter(admin_repayment=kwargs['admin_repayment']).order_by('created_at')
        return queryset


class RepaymentFragment(models.Model):
    """
    Abstraction for a fragment of a repayment from a project that belongs to a
    particular RevolvUserProfile.

    A RepaymentFragment represents the proportional amount of money that the
    associated user is repayed for an AdminRepayment to a project. In other
    words, for user U, project P, and AdminRepayment R, the amount of the
    RepaymentFragment for U will be:

        ((U's donation to P) / (Total organic donations to P)) * R.amount

    When a RepaymentFragment is generated/deleted, we automatically
    increment/decrement the pool of reinvestable money in the related user.

    RepaymentFragments are generated automatically when an AdminRepayment is
    created.  RepaymentFragments should never be created manually!

    ::Signals::
    post_save
        When a RepaymentFragment is saved, we increment the reinvest_pool in the
        related user.
    pre_delete
        Before a RepaymentFragment is deleted, we decrement the reinvest_pool in
        the related user.
    """
    user = models.ForeignKey('base.RevolvUserProfile')
    project = models.ForeignKey("project.Project")
    admin_repayment = models.ForeignKey(AdminRepayment)

    amount = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    objects = RepaymentFragmentManager()
    factories = ImportProxy("revolv.payments.factories", "RepaymentFragmentFactories")

    def __unicode__(self):
        return '%s to %s for %s' % (self.amount, self.user, self.project)


class UserReinvestmentManager(models.Manager):
    """
    Manager for UserReinvestment.
    """

    def reinvestments(self, user=None, project=None, queryset=None):
        """
        :return: UserReinvestment associated with this project.
        """
        if queryset is None:
            queryset = super(UserReinvestment, self).get_queryset()
        if user:
            queryset = queryset.filter(user=user).order_by('created_at')
        if project:
            queryset = queryset.filter(project=project).order_by('created_at')
        return queryset


class UserReinvestment(models.Model):
    """
    Model representing a single, "contact point" for a
    reinvestment by user himself.

    User only can do reinvestment if he is on reinvestment period (usually before
    15th day of a running month).

    And An UserReinvestment cannot be created if there are insufficient funds.

    ::Signals::
    pre_init
        Raises a NotEnoughFundingException before __init__ if there are not
        enough funds for this UserReinvestment or not in reinvestment period.
    pre_save
        We'll cap the investment here, by monthly allocation and founding_goal
    post_save
        Send to payment
    """
    amount = models.FloatField()
    user = models.ForeignKey('base.RevolvUserProfile')
    project = models.ForeignKey("project.Project")

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserReinvestmentManager()
    factories = ImportProxy("revolv.payments.factories", "UserReinvestmentFactory")


class PaymentManager(models.Manager):
    """
    Simple manager for the Payment model.
    """

    def payments(self, user=None, entrant=None, project=None, queryset=None):
        """
        :return: Payments associated with this user and project
        """
        if queryset is None:
            queryset = super(PaymentManager, self).get_queryset()
        if user:
            queryset = queryset.filter(user=user).order_by('created_at')
        if entrant:
            queryset = queryset.filter(entrant=entrant).order_by('created_at')
        if project:
            queryset = queryset.filter(project=project).order_by('created_at')
        return queryset

    def donations(self, user=None, project=None, queryset=None, organic=False):
        """
        :kwargs:
            user: filter donations by this user
            project: filter donations by this project
            queryset: further filtering of Payments
            organic: if True, indicates that this method should only return
                Payments for which the `user` and the `entrant` columns are both
                non-null and the same

        :return:
            Returns all payments that are not reinvestment_fragments associated
            with this user.
        """
        donations = self.payments(
            user=user,
            project=project,
            queryset=queryset
        ).exclude(
            payment_type__name=PaymentType._REINVESTMENT
        )

        if organic:
            if user:
                donations = donations.filter(entrant=user)
            else:
                donations = donations.exclude(user__isnull=True).filter(
                    entrant__pk=models.F('user__pk'))

        return donations

    def reinvestment_fragments(self, user=None, project=None, queryset=None):
        """
        :return:
            Returns all reinvestment_fragment payments that are associated with
            this user.
        """
        return self.payments(
            user=user,
            project=project,
            queryset=queryset
        ).filter(
            payment_type__name=PaymentType._REINVESTMENT
        )

    def project_reinvestment_from_date(self, project=None, from_date=None,
                                       queryset=None):
        """
        :return:
            Returns all reinvestment_fragment payments that are associated with
            this user.
        """
        q = self.payments(
            project=project,
            queryset=queryset
        ).filter(
            payment_type__name=PaymentType._REINVESTMENT
        )
        if from_date:
            q = q.filter(created_at__gte=from_date)
        return q

    def repayment_fragments(self, user=None):
        """
        :return:
            Returns all the repayment_fragment payments that are associated with
            this user.
        """
        return RepaymentFragment.objects.filter(user=user)

    def repayments(self, user, admin=None, project=None, queryset=None):
        """
        :return:
            Returns all the repayments that are associated with this user.
        """
        return AdminRepayment.objects.filter(
            revolvuserprofiles__in=user, projects__in=project
        ).distinct()

    def total_distinct_organic_donors(self, queryset=None):
        """
        :return:
            The total number of organic donors that have ever donated to a
            RE-volv project. Useful for displaying stats on the homepage.
            Organic donors are donors that have made a
            non-'reinvestment_fragment'-type payment to this project. Organic
            donors also do not include 'check'-type payments for which there
            is no user.
        """
        if queryset is None:
            queryset = self.donations()
        num_users = queryset.values("user").distinct().count()
        return num_users

    def total_reinvestment_amount(self, user=None, project=None, queryset=None):
        """
        :kwargs:
            user: filter donations by this user
            project: filter donations by this project
            queryset: further filtering of Payments

        :return:
            Returns the total amount reinvested for a specified user or project or both.
        """
        total_amount = self.reinvestment_fragments(user, project, queryset).aggregate(
            models.Sum('amount')
        )['amount__sum']
        if total_amount is None:
            return 0
        else:
            return total_amount

    def total_project_reinvestment_from_date(self, project=None, from_date=None,
                                             queryset=None):
        """
        :kwargs:
            user: filter donations by this user
            project: filter donations by this project
            queryset: further filtering of Payments

        :return:
            Returns the total amount reinvested for a specified user or project or both.
        """
        total_amount = self.project_reinvestment_from_date(project=project,
                                                           from_date=from_date,
                                                           queryset=queryset)\
            .aggregate(models.Sum('amount'))['amount__sum']

        if total_amount is None:
            return 0
        else:
            return total_amount


class Payment(models.Model):
    """
    Abstraction indicating one particular payment.

    A Payment represents only money flowing from a user to a project, not the
    other way around. RepaymentFragment is a separate model representing the
    reverse.

    ::Signals::
    post_save
        If the payment is organic, we add this payment's user as a donor
        to the related project. If the payment is a reinvestment_fragment, we decrement
        the reinvest_pool in the related user.
    pre_delete
        If the payment is organic, we remove this payment's user as a donor to
        the related project if he has no other payments to that project.  If the
        payment is a reinvestment_fragment, we decrement the reinvest_pool in the related
        user. Reinvestment money originates from repayments made by
        already completed projects.
    """
    user = models.ForeignKey('base.RevolvUserProfile', blank=True, null=True)
    project = models.ForeignKey("project.Project")

    entrant = models.ForeignKey('base.RevolvUserProfile', related_name='entrant')
    payment_type = models.ForeignKey(PaymentType)
    created_at = models.DateTimeField(auto_now_add=True)

    admin_reinvestment = models.ForeignKey(AdminReinvestment, blank=True, null=True)
    user_reinvestment = models.ForeignKey(UserReinvestment, blank=True, null=True)

    amount = models.FloatField()

    objects = PaymentManager()
    factories = ImportProxy("revolv.payments.factories", "PaymentFactories")

    @property
    def is_organic(self):
        return self.user == self.entrant

    def __unicode__(self):
        return '%s from %s for %s' % (self.amount, self.user, self.project)


class ProjectMontlyRepaymentConfig(models.Model):
    """
    A Model contains configuration distribution of repayment.

    Repayment will be spilt by 2: for Solar Seed fund(SSF) and for RE-volv overhead.
    We'll used value on SSF for calculating fund to reinvestmentm each month
    """
    SOLAR_SEED_FUND = 'SSF'
    REVOLVE_OVERHEAD = 'REV'
    REPAYMENT_TYPE_CHOICES = ((SOLAR_SEED_FUND, 'Solar Seed Fund'), (REVOLVE_OVERHEAD, 'RE-volv Overhead'))

    project = models.ForeignKey("project.Project")
    year = models.PositiveSmallIntegerField(default=date.today().year)
    repayment_type = models.CharField(max_length=3, choices=REPAYMENT_TYPE_CHOICES)
    amount = models.FloatField()
    factories = ImportProxy('revolv.payments.factories', 'ProjectMontlyRepaymentConfigFactory')

    def __unicode__(self):
        return '%s %s in %s for %s' % (self.repayment_type, self.amount, self.year, self.project)


class Tip(models.Model):
    """
        Percentage of payment user elects to add to donation toward Revolv overhead costs
    """
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey('base.RevolvUserProfile')
    amount = models.FloatField()
