from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email
from revolv.settings import SITE_URL

from django.core.urlresolvers import reverse
from sesame import utils


def user_reinvestment_reminder():
    """
    Mail worker
    """
    project_reinvest_list_url = SITE_URL + reverse('project:reinvest_list')
    unsubscribe_update_url = SITE_URL + reverse('unsubscribe_updates')
    for user in RevolvUserProfile.objects.filter(reinvest_pool__gt=0.0, subscribed_to_updates=True):
        data = dict()
        data['amount'] = user.reinvest_pool
        data['projects_url'] = project_reinvest_list_url + utils.get_query_string(user.user)
        data['unsubscribe_url'] = unsubscribe_update_url + utils.get_query_string(user.user)
        data['first_name'] = user.user.first_name
        send_revolv_email(
            'reinvestment_reminder',
            data, [user.user.email]
        )