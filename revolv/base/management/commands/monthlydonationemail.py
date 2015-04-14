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
        make_option('--silence_admin_notifications',
                    action='store_true',
                    dest='silence_admin_notifications',
                    default=False,
                    help='Silences any administrator notifications that the monthlydonationemail command was run.'),
    )

    def handle(self, *args, **options):
        """
        This handle function is run when the command "python manage.py monthlydonationemail"
        is typed into the command line.

        To run it on any day which is not the first day, use "python manage.py monthlydonationemail --override".

        To silence email notifications to administrators as well, add the "--silence_admin_notifications" flag.

        It iterates through all users, and sends a monthly donation email to any user who donated
        in the last month. (Specifically the last month, not the last 30 days, it it is run on 4/4,
        it'll email users who donated on 3/1 but not on 4/2.) It by default will also send an email
        notification to all administrators.

        """
        if timezone.now().day == 1 or options['override']:  # checks if the it is the first day of the month
            print "Running monthlydonationemail command on " + str(timezone.now()) + "."
            revolv_user_profiles = RevolvUserProfile.objects.all()
            num_emails_sent = 0
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
                    num_emails_sent = num_emails_sent + 1
            # Sends an email notification to administrators
            if not options['silence_admin_notifications']:
                context = {}
                context['emails_sent'] = num_emails_sent
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
