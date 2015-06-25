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

def aggregate_stats(user_profile):
    """Aggregates statistics about a Re-volv user's impact and returns a dictionary with 
    these values. These values are later presented on the user's dashboard.
    """
    stat_dict = {}
    stat_dict['project_count'] = Project.objects.donated_projects(user_profile).count()
    stat_dict['repayments'] = Payment.objects.repayment_fragments(user=user_profile).aggregate(Sum('amount'))['amount__sum'] or 0
    all_payments = Payment.objects.payments(user=user_profile)
    stat_dict['trees'] = user_profile.get_statistic_for_user("acres_of_trees_saved_per_year", all_payments)
    stat_dict['kwh'] = user_profile.get_statistic_for_user("kilowatt_hours_per_month", all_payments)
    stat_dict['carbon_dioxide'] = user_profile.get_statistic_for_user("pounds_carbon_saved_per_month", all_payments)
    return stat_dict