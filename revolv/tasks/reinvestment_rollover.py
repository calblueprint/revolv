__author__ = 'deedee'
from revolv.project.models import Project, ProjectProperty
from revolv.payments.models import ProjectMontlyRepaymentConfig, AdminReinvestment
from revolv.base.models import RevolvUserProfile
from revolv.settings import ADMIN_PAYMENT_ID

from django.db.models import Sum
from celery.task import task
from datetime import date

@task
def distribute_reinvestment_fund():

    try:
        admin = RevolvUserProfile.objects.get(id=ADMIN_PAYMENT_ID)
    except admin.DoesNotExist:
        pass#exit

    for project in Project.get_project_reinvested_amount_by_user():
        cap = project.get_reinvestment_cap() - project.amount_reinvested
        remaining = project.amount_left()
        amount_to_reinvest = cap if remaining > cap else remaining
        AdminReinvestment.objects.create(
            amount=amount_to_reinvest,
            admin=admin,
            project=project
        )






