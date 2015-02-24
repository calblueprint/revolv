from django.contrib.auth.models import User
from django.db import models

from django_facebook.models import FacebookModel
from revolv.base.utils import get_group_by_name, get_profile


class RevolvUserProfileManager(models.Manager):
    def create_user(self, *args, **kwargs):
        """
        For purposes of testing and DRYness, it is often useful to create
        a user and return the associated RevolvUserProfile.
        """
        user = User.objects.create_user(*args, **kwargs)
        return get_profile(user)

    def create_user_as_admin(self, *args, **kwargs):
        """Create a user, assign it to be an admin, and return its profile."""
        profile = self.create_user(*args, **kwargs)
        profile.make_administrator()
        return profile


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
    approved by the admin.

    Admins are users who can approve and manage projects, AND control whether
    other users are ambassadors or admins themselves. Admins can also donate to
    projects like regular donors can.
    """
    objects = RevolvUserProfileManager()

    AMBASSADOR_GROUP = "ambassadors"
    ADMIN_GROUP = "administrators"

    user = models.OneToOneField(User)
    subscribed_to_newsletter = models.BooleanField(default=False)

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

    def make_ambassador(self):
        self.user.groups.remove(get_group_by_name(self.ADMIN_GROUP))
        self.user.groups.add(get_group_by_name(self.AMBASSADOR_GROUP))

    def make_donor(self):
        """Take away all the user's permissions."""
        self.user.groups.remove(get_group_by_name(self.ADMIN_GROUP))
        self.user.groups.remove(get_group_by_name(self.AMBASSADOR_GROUP))
