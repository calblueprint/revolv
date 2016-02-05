from revolv.project.models import Project
from revolv.payments.models import ProjectMontlyRepaymentConfig, AdminRepayment
from revolv.base.models import RevolvUserProfile
from revolv.tasks.monthly_reminders import user_reinvestment_reminder
from django.conf import settings
from django.db.models import Sum
from celery.task import task
from datetime import date

import logging
import sys
import time

logger = logging.getLogger(__name__)


@task
def calculate_montly_reinvesment_allocation():
    """
    This task to handle month reinvestment calculation

    This is how it do:
    1. Calculate money in out hand: balance + sum of incomming installment
    2. Calculate max money to re-allocate to each active project
    3. Set project monthly_reinvestment_cap with above value
    4. Send email alert to user
    """
    ADMIN_PAYMENT_USERNAME = settings.ADMIN_PAYMENT_USERNAME
    logger.info('Calculate monthly allocation')
    try:
        admin = RevolvUserProfile.objects.get(user__username=ADMIN_PAYMENT_USERNAME)
    except RevolvUserProfile.DoesNotExist:
        logger.error("Can't find admin user: {0}. System exiting!".format(ADMIN_PAYMENT_USERNAME))
        sys.exit()

    reinvest_balance = RevolvUserProfile.objects.all().aggregate(total=Sum('reinvest_pool'))['total']
    logger.info('Current reinvestment balance: %s' % reinvest_balance)
    for project in Project.objects.get_completed_unpaid_off_projects():
        try:
            repayment_config = project.projectmontlyrepaymentconfig_set\
                .get(year=date.today().year, repayment_type=ProjectMontlyRepaymentConfig.SOLAR_SEED_FUND)
        except ProjectMontlyRepaymentConfig.DoesNotExist:
            logger.error("Project {0} - {%} doesn't have repayment config!".format(project.id, project.title))

        AdminRepayment.objects.create(amount=repayment_config.amount,
                                      project=project,
                                      admin=admin)
        reinvest_balance += repayment_config.amount

    if reinvest_balance < 0.0:
        logger.info("We don't have any balance. Exiting")
        sys.exit()

    logger.info('Total reinvestment balance: %s' % reinvest_balance)

    recipient = filter(lambda p: p.amount_left > 0.0, Project.objects.get_active())

    logger.info('Total project active: %s' % len(recipient))

    fund_per_recipient = reinvest_balance / len(recipient)
    logger.info('Fund allocated to each project: %s' % fund_per_recipient)
    for project in recipient:
        project.monthly_reinvestment_cap = fund_per_recipient
        project.save()
    #wait for 30s and the send mail
    time.sleep(30)

    user_reinvestment_reminder()
