from django.core.management.base import BaseCommand

from revolv.base.models import RevolvUserProfile


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('WHAT IS UP')
        revolv_user_profiles = RevolvUserProfile.objects.all()
        for revolv_user_profile in revolv_user_profiles:
            donation_set = revolv_user_profile.payment_set.all()
            if len(donation_set) > 0:
                for donation in donation_set:
                    self.stdout.write(str(donation.amount))
