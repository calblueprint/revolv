__author__ = 'deedee'

from revolv.project.models import Project, ProjectProperty
from revolv.payments.models import ProjectMontlyRepaymentConfig, AdminReinvestment
from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email
from revolv.settings import BASE_URL

from django.core.urlresolvers import reverse
from sesame import utils

from celery.task import task
from datetime import date


@task
def user_reinvestment_reminder():
    project_reinvest_list_url = BASE_URL + reverse('project:reinvest_list')
    unsubscribe_update_url = BASE_URL + reverse('unsubscribe_updates')
    for user in RevolvUserProfile.objects.filter(reinvest_pool__gt=0.0):
        data = {}
        data['amount'] = user.reinvest_pool
        data['projects_url'] = project_reinvest_list_url + utils.get_query_string(user.user)
        data['unsubscribe_url'] = unsubscribe_update_url + utils.get_query_string(user.user)
        data['first_name'] = user.user.first_name
        send_revolv_email(
            'reinvestment_reminder',
            data, [user.user.email]
        )