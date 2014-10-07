from django.contrib.auth.models import User
from django.db import models
from django_facebook.models import FacebookModel


class RevolvUserProfile(FacebookModel):
    """
    A simple wrapper around django-facebook's FacebookModel, which contains
    Facebook information like name, etc. RevolvUserProfile ties a FacebookModel
    and a django auth.User model together, so that we can use both Facebook
    and non-Facebook user profiles.
    """
    user = models.OneToOneField(User)
