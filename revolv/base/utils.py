from collections import namedtuple

from django.conf import settings
from django.contrib.auth.models import Group, User
import datetime


"""
An abstraction for a classification of grouped projects which have a string that
the group displays as, e.g. "Proposed Projects" and a unique key which we can use
to refer to the group, e.g. "proposed".
"""
ProjectGroup = namedtuple("ProjectGroup", ["display", "key"])


def get_profile(user):
    return user.revolvuserprofile


def get_group_by_name(group_name):
    """Return the relevant django.contrib.auth.models.Group, or error."""
    return Group.objects.get(name=group_name)


def get_all_administrators():
    """Return a queryset of all admin users."""
    return User.objects.filter(groups__name="administrators")


def get_all_administrator_emails():
    return [data["email"] for data in get_all_administrators().values("email")]


def is_user_reinvestment_period():
    """
    :return: True if now is in user reinvestment period
    """
    return True if datetime.datetime.now() < settings.ADMIN_REINVESTMENT_DATE_DT else False
