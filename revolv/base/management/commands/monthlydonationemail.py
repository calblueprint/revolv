from django.core.management.base import BaseCommand

from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email


class Command(BaseCommand):
    """
    This handle function is the logic that is run when the command
    python manage.py monthlydonationemail is typed into the command line.

    It finds all users, goes through them, and sends a monthly donation
    email to anyone who has donated in the past month
    """

    def handle(self, *args, **options):
        revolv_user_profiles = RevolvUserProfile.objects.all()
        for revolv_user_profile in revolv_user_profiles:
            donation_set = revolv_user_profile.payment_set.all()
            if len(donation_set) > 0:
                context = {}
                user = revolv_user_profile.user
                context['user'] = user
                context['payments'] = donation_set
                send_revolv_email(
                    'monthly_donation_email',
                    context, [user.email]
                )
