__author__ = 'deedee'
from revolv.project.models import Project, ProjectProperty
from revolv.payments.models import ProjectMontlyRepaymentConfig, AdminReinvestment
from revolv.base.models import RevolvUserProfile
from revolv.settings import ADMIN_PAYMENT_USERNAME

from celery.task import task

import sys
import logging

logger = logging.getLogger("revolv")


@task
def distribute_reinvestment_fund():
    """
    This task is to Automatic reinvestment
    """
    try:
        admin = RevolvUserProfile.objects.get(user__username=ADMIN_PAYMENT_USERNAME)
    except RevolvUserProfile.DoesNotExist:
        logger.error("Can't find admin user: {0}. System exiting!".format(ADMIN_PAYMENT_USERNAME))
        sys.exit()

    for project in Project.objects.get_eligible_projects_for_reinvestment():
        amount_to_reinvest = project.reinvest_amount_left if project.reinvest_amount_left < project.amount_left else \
            project.amount_left
        if amount_to_reinvest > 0.0:
            logger.info('Trying to reinvest {0} to {1}-{2}'.format(amount_to_reinvest, project.id, project.title))
            AdminReinvestment.objects.create(
                amount=amount_to_reinvest,
                admin=admin,
                project=project
            )
        project.disable_reinvestment()
        ProjectProperty.objects.filter(project=project, name=ProjectProperty.REINVESTMENT_CAP).\
            update(value='0.0')







