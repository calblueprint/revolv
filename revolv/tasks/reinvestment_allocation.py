__author__ = 'deedee'

from revolv.project.models import Project, ProjectProperty
from revolv.payments.models import ProjectMontlyRepaymentConfig, AdminRepayment
from revolv.base.models import RevolvUserProfile
from revolv.settings import ADMIN_PAYMENT_ID

from django.db.models import Sum
from celery.task import task
from datetime import date

@task
def calculate_montly_reinvesment_allocation():
    try:
        admin = RevolvUserProfile.objects.get(id=ADMIN_PAYMENT_ID)
    except admin.DoesNotExist:
        pass#exit

    reinvest_balance = RevolvUserProfile.objects.all().aggregate(total=Sum('reinvest_pool'))

    for project in Project.objects.get_completed_unpaid_off_projects():
        try:
            repayment_config = project.projectmontlyrepaymentconfig_set\
                .get(year=date.today().year, repayment_type=ProjectMontlyRepaymentConfig.SOLAR_SEED_FUND)
        except repayment_config.DoesNotExist:
            #log
            pass

        AdminRepayment.objects.create(amount=repayment_config.amount,
                                      project=project,
                                      admin=admin)
        reinvest_balance += repayment_config.amount

    recipient = Project.objects.get_eligible_projects_for_reinvestment()
    fund_per_recipient = reinvest_balance / recipient.count()
    str_fund_per_recipient = str(fund_per_recipient)
    for project in recipient:
        try:
            asset = project.projectproperty_set.get(name=ProjectProperty.REINVESTMENT_CAP)
        except asset.DoesNotExist:
            asset = ProjectProperty(name=ProjectProperty.REINVESTMENT_CAP)
        except asset.MultipleObjectsReturned:
            project.projectproperty_set.all().delete()
            asset = ProjectProperty(name=ProjectProperty.REINVESTMENT_CAP)

        asset.value = str_fund_per_recipient
        asset.save()
