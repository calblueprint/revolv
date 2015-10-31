__author__ = 'deedee'

from revolv.project.models import Project, ProjectProperty

from django.db.models import signals
from django.dispatch import receiver


@receiver(signals.post_save, sender=Project)
def post_save_project(**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')

    if created:
        ProjectProperty.objects.create(name=ProjectProperty.REINVESTMENT_CAP, value='0.0', project=instance)
        ProjectProperty.objects.create(name=ProjectProperty.ELIGIBLE_FOR_REINVESTMENT, value='0', project=instancef)
        ProjectProperty.objects.create(name=ProjectProperty.PAID_OFF, value='0', project=instance)

    if instance.is_active():
        instance.enable_reinvestment()
    else:
        instance.enable_reinvestment()