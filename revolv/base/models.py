from django.contrib.auth.models import User
from django.db import models
from django_facebook.models import FacebookModel
from revolv.base.utils import get_group_by_name, get_profile
from revolv.lib.utils import ImportProxy
from revolv.payments.models import Payment

class RevolvUserProfileManager(models.Manager):
    def create_user(self, *args, **kwargs):
        """
        For purposes of testing and DRYness, it is often useful to create
        a user and return the associated RevolvUserProfile.
        """
        user = User.objects.create_user(*args, **kwargs)
        return get_profile(user)

    def create_user_as_ambassador(self, *args, **kwargs):
        """Create a user, assign it to be an ambassador, and return its profile."""
        profile = self.create_user(*args, **kwargs)
        profile.make_ambassador()
        return profile

    def create_user_as_admin(self, *args, **kwargs):
        """Create a user, assign it to be an admin, and return its profile."""
        profile = self.create_user(*args, **kwargs)
        profile.make_administrator()
        return profile

    def get_subscribed_to_newsletter(self, queryset=None):
        """ Gets all the RevolvUserProfile objects that are
        currently subscribed to the newsletter. It also orders the queryset
        by order which the user joined.

        :queryset: The queryset in which to search for users
        :return: A queryset of RevolvUserProfile objects sorted by date joined
        """
        if queryset is None:
            queryset = super(RevolvUserProfileManager, self).get_queryset()
        subscribed_users = queryset.filter(
            subscribed_to_newsletter=True
        ).order_by('user__date_joined')
        return subscribed_users


class RevolvUserProfile(FacebookModel):
    """
    A simple wrapper around django-facebook's FacebookModel, which contains
    Facebook information like name, etc. RevolvUserProfile ties a FacebookModel
    and a django auth.User model together, so that we can use both Facebook
    and non-Facebook user profiles.

    Note: there are three main roles that users in the Revolv application can
    occupy: donor, ambassador, and admin.

    Donors are regular users, who can donate to projects and see the impact of
    their donations.

    Ambassadors are users who can donate AND create projects, to be
    approved by the admin. Note: ambassadors are NOT staff with respect to the
    django User model, since we use the is_staff boolean to check whether the
    django CMS toolbar is visible for users.

    Admins are users who can approve and manage projects, AND control whether
    other users are ambassadors or admins themselves. Admins can also donate to
    projects like regular donors can. Every admin's User model has is_staff = True
    in order to see the django-cms toolbar on the homepage.
    """
    objects = RevolvUserProfileManager()
    factories = ImportProxy("revolv.base.factories", "RevolvUserProfileFactories")

    AMBASSADOR_GROUP = "ambassadors"
    ADMIN_GROUP = "administrators"

    user = models.OneToOneField(User)
    subscribed_to_newsletter = models.BooleanField(default=False)
    subscribed_to_updates = models.BooleanField(default=True)

    reinvest_pool = models.FloatField(default=0.0)
    preferred_categories = models.ManyToManyField("project.Category")

    address = models.CharField(max_length=255, null=True, blank=True)

    def is_donor(self):
        """Return whether the associated user can donate."""
        return True

    def is_ambassador(self):
        return get_group_by_name(
            self.AMBASSADOR_GROUP
        ) in self.user.groups.all()

    def is_administrator(self):
        return get_group_by_name(self.ADMIN_GROUP) in self.user.groups.all()

    def make_administrator(self):
        self.user.groups.add(get_group_by_name(self.AMBASSADOR_GROUP))
        self.user.groups.add(get_group_by_name(self.ADMIN_GROUP))
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()

    def make_ambassador(self):
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.groups.remove(get_group_by_name(self.ADMIN_GROUP))
        self.user.groups.add(get_group_by_name(self.AMBASSADOR_GROUP))
        self.user.save()

    def make_donor(self):
        """Take away all the user's permissions."""
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.groups.remove(get_group_by_name(self.ADMIN_GROUP))
        self.user.groups.remove(get_group_by_name(self.AMBASSADOR_GROUP))
        self.user.save()

    def get_statistic_for_user(self, attr):
        """Calculates a user's individual impact by iterating through all the users payments, calculating
        what fraction of that project comprises of this user's donation, and calculates individual
        user impact using the statistics attribute (a KilowattStatsAggregator) and the fraction."""
        all_payments = Payment.objects.payments(user=self)
        user_impact = 0
        for payment in all_payments:
            project = payment.project
            user_financial_contribution = payment.amount
            project_funding_total = (int)(project.funding_goal)
            project_impact = getattr(project.statistics, attr)
            user_impact_for_project = project_impact * user_financial_contribution * 1.0 / project_funding_total
            user_impact += user_impact_for_project
        return user_impact

    def get_full_name(self):
        name = '{0} {1}'.format(self.user.first_name.strip(), self.user.last_name.strip())
        if len(name.strip()) == 0:
            name = self.user.username
        return name
