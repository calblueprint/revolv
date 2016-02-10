from django.conf import settings

from revolv.project.models import Project
from revolv.payments.models import ProjectMontlyRepaymentConfig, AdminReinvestment
from revolv.base.models import RevolvUserProfile

from celery.task import task

import sys
import time
import logging

logger = logging.getLogger("revolv")


@task
def distribute_reinvestment_fund():
    """
    This task is for Automatic reinvestment

    This is how tis script do:
    1. Get all project that is eligible for reinvestment:
        (project with monthly_reinvestment_cap >0 and not fully funded)
    2. For each project determine how we'll reinvest ( min(monthly_reinvestment_cap, amount_left)
    3. Add AdminReinvestment object with above value
    4. Set monthly_reinvestment_cap to 0.0
    """

    time.sleep(60)
    ADMIN_PAYMENT_USERNAME = settings.ADMIN_PAYMENT_USERNAME

    try:
        admin = RevolvUserProfile.objects.get(user__username=ADMIN_PAYMENT_USERNAME)
    except RevolvUserProfile.DoesNotExist:
        logger.error("Can't find admin user: {0}. System exiting!".format(ADMIN_PAYMENT_USERNAME))
        sys.exit()

    for project in Project.objects.get_eligible_projects_for_reinvestment():
        amount_to_reinvest = project.reinvest_amount_left
        if amount_to_reinvest > 0.0:
            logger.info('Trying to reinvest {0} to {1}-{2}'.format(amount_to_reinvest, project.id, project.title))
            AdminReinvestment.objects.create(
                amount=amount_to_reinvest,
                admin=admin,
                project=project
            )
        project.monthly_reinvestment_cap = 0.0
        project.save()
