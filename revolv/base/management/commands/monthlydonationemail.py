import datetime
from optparse import make_option

from django.core.management.base import BaseCommand

from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email


class Command(BaseCommand):
    # for adding the override command to monthlydonationemail
    option_list = BaseCommand.option_list + (
        make_option('--override',
                    action='store_true',
                    dest='override',
                    default=False,
                    help='Override to run on a day which is not the first of the month'),
    )

    def handle(self, *args, **options):
        """
        This handle function is run when the command "python manage.py monthlydonationemail"
        is typed into the command line.

        To run it on any day which is not the first day, use "python manage.py monthlydonationemail --override"

        It iterates through all users, and sends a monthly donation email to any user
        who has donated in the past month.
        """
        if datetime.date.today().day == 1 or options['override']:  # checks if the it is the first day of the month
            print "Running monthlydonationemail command on " + str(datetime.date.today())
            revolv_user_profiles = RevolvUserProfile.objects.all()
            for revolv_user_profile in revolv_user_profiles:
                donation_set = revolv_user_profile.payment_set.all()
                donation_set = get_last_month_donations(donation_set)
                if len(donation_set) > 0:
                    context = {}
                    user = revolv_user_profile.user
                    context['user'] = user
                    context['payments'] = donation_set
                    send_revolv_email(
                        'monthly_donation_email',
                        context, [user.email]
                    )
        else:
            print "Attempted to run monthlydonationemail command on a day that was not the 1st of the month"


def get_last_month_donations(donation_set):
    """
    This helper function filters a donation set to only include donations from
    the last month.

    i.e., If the current month is April, filters and returns all donations from March
    """
    # gets a day from the last month
    date_of_last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    # gets the year and month corresponding to the previous month
    last_month = date_of_last_month.month
    year = date_of_last_month.year
    return [donation for donation in donation_set if last_month == donation.created_at.month and year == donation.created_at.year]
