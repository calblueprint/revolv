from django.db.models import Sum
from revolv.payments.models import Payment
from revolv.project.models import Project

def get_solar_csv_url(csv_id, mode):
    """Gets request url to export csv for project with that id.
    Mode represents daily, monthly or annual values based on whether
    it is 1, 2, or 3 respectively."""

    url = "http://home.solarlog-web.net/sds/modul/SolarLogWeb/Statistik.php?logid=0&c="
    url += csv_id + "&mode=" + str(mode) + "&offset=0&flag=32&ex=csv"
    return url

def get_statistic_for_user(user_profile, attr):
    """Calculates a user's individual impact by iterating through all the users payments, calculating
    what fraction of that project comprises of this user's donation, and calculates individual
    user impact using the statistics attribute (a KilowattStatsAggregator) and the fraction.
    """
    all_payments = Payment.objects.payments(user=user_profile)
    user_impact = 0
    for payment in all_payments:
        project = payment.project
        user_financial_contribution = payment.amount
        project_funding_total = (int)(project.funding_goal)
        project_impact = getattr(project.statistics, attr)
        user_impact_for_project = project_impact*user_financial_contribution*1.0/project_funding_total
        user_impact += user_impact_for_project
    return user_impact

def aggregate_stats(user_profile):
    """Aggregates statistics about a Re-volv user's impact and returns a dictionary with 
    these values. These values are later presented on the user's dashboard.
    """
    stat_dict = {}
    stat_dict['project_count'] = Project.objects.donated_projects(user_profile).count()
    stat_dict['repayments'] = Payment.objects.repayment_fragments(user=user_profile).aggregate(Sum('amount'))['amount__sum'] or 0
    stat_dict['trees'] = get_statistic_for_user(user_profile, "acres_of_trees_saved_per_year")
    stat_dict['kwh'] = get_statistic_for_user(user_profile, "kilowatt_hours_per_month")
    stat_dict['carbon_dioxide'] = get_statistic_for_user(user_profile, "pounds_carbon_saved_per_month")
    return stat_dict