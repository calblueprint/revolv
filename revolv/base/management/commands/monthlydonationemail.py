import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone

from revolv.base.models import RevolvUserProfile
from revolv.base.utils import get_all_administrator_emails
from revolv.lib.mailer import send_revolv_email


class Command(BaseCommand):
    # for adding the override and emailadmins command to monthlydonationemail
    option_list = BaseCommand.option_list + (
        make_option('--override',
                    action='store_true',
                    dest='override',
                    default=False,
                    help='Override to run on a day which is not the first of the month.'),
    ) + (
        make_option('--emailadmins',
                    action='store_true',
                    dest='emailadmins',
                    default=False,
                    help='Email administrators sends a notification that the monthlydonationemail command was run.'),
    )

    def handle(self, *args, **options):
        """
        This handle function is run when the command "python manage.py monthlydonationemail"
        is typed into the command line.

        To run it on any day which is not the first day, use "python manage.py monthlydonationemail --override"

        To send a email notification to administrators as well, add the "--emailadmins" flag.

        It iterates through all users, and sends a monthly donation email to any user
        who has donated in the past month.
        """
        if timezone.now().day == 1 or options['override']:  # checks if the it is the first day of the month
            print "Running monthlydonationemail command on " + str(timezone.now()) + "."
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
            # Sends an email notification to administrators if the flag is enabled
            if options['emailadmins']:
                send_revolv_email(
                    'monthly_donation_email_admin_notification',
                    context, get_all_administrator_emails()
                )
        else:
            print "monthlydonationemail command was not run. Use --override to run it if it is currently not the first of the month."


def get_last_month_donations(donation_set):
    """
    This helper function filters a donation set to only include donations from
    the last month.

    i.e., If the current month is April, filters and returns all donations from March
    """
    # gets a day from the last month
    date_of_last_month = timezone.now().replace(day=1) - datetime.timedelta(days=1)
    # gets the year and month corresponding to the previous month
    last_month = date_of_last_month.month
    year = date_of_last_month.year
    return [donation for donation in donation_set if last_month == donation.created_at.month and year == donation.created_at.year]
