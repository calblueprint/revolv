import datetime

from django.core.management.base import BaseCommand

from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email


class Command(BaseCommand):
    """
    This handle function is run when the command "python manage.py monthlydonationemail"
    is typed into the command line.

    It iterates through all users, and sends a monthly donation email to any user
    who has donated in the past month
    """

    def handle(self, *args, **options):
        if datetime.date.today().day == 1:  # checks if the it is the first day of the month
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


"""
This helper function filters a donation set to only include donations from
the last month.

i.e., If the current month is April, filters and returns all donations from March
"""


def get_last_month_donations(donation_set):
    # gets a day from the last month
    date_of_last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    # gets the year and month corresponding to the previous month
    last_month = date_of_last_month.month
    year = date_of_last_month.year
    return [donation for donation in donation_set if last_month == donation.created_at.month and year == donation.created_at.year]
