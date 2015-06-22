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
    return stat_dict