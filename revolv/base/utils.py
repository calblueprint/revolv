from collections import namedtuple

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

def get_first_date_of_month():
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, 1)

def get_current_year():
    return datetime.datetime.now().year

def get_admin_reinvestment_date(d):
    now = datetime.datetime.now()
    return datetime.datetime(now.year, now.month, d[0], d[1], d[2])
