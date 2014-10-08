from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from django_facebook.utils import get_user_model
from revolv.base.models import RevolvUserProfile


@receiver(post_save, sender=get_user_model())
def create_profile_of_user(sender, instance, created, **kwargs):
    """When a User model is created, create a corresponding RevolvUserProfile.
    """
    if created:
        RevolvUserProfile.objects.get_or_create(user=instance)


@receiver(post_delete, sender=get_user_model())
def delete_profile_of_user(sender, instance, **kwargs):
    """
    When a User model is deleted, also delete the corresponding
    RevolvUserProfile.
    """
    try:
        RevolvUserProfile.objects.get(user=instance).delete()
    except:
        pass
