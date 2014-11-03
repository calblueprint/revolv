from django.contrib.auth.models import Group


def get_profile(user):
    return user.revolvuserprofile


def get_group_by_name(group_name):
    """Return the relevant django.contrib.auth.models.Group, or error."""
    return Group.objects.get(name=group_name)
