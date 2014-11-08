from django.contrib.auth.models import Group, User


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
