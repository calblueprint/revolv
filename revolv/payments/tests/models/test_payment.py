from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from django_facebook.utils import get_user_model
from revolv.base.models import RevolvUserProfile
from revolv.base.signals import create_profile_of_user
from revolv.payments.models import Payment, PaymentInstrumentType
from revolv.project.models import Project


class PaymentTest(TestCase):
    reinvestment = PaymentInstrumentType.objects.get_reinvestment()
    repayment = PaymentInstrumentType.objects.get_repayment()

    def setUp(self):
        post_save.disconnect(create_profile_of_user, sender=get_user_model())
        call_command('loaddata', 'user', 'revolvuserprofile', 'project')

    def tearDown(self):
        post_save.connect(create_profile_of_user, sender=get_user_model())

    def _create_payment(self, user, project=None, instrument_type=None):
        if project is None:
            project = Project.objects.get(id=1)
        if instrument_type is None:
            instrument_type = PaymentInstrumentType.objects.get_paypal()
        return Payment(amount=10.00, user=user, entrant=user, payment_instrument_type=instrument_type, project=project)

    def test_payment_create(self):
        """Verify that the payment can be created."""
        user = RevolvUserProfile.objects.get(id=1)
        self._create_payment(user).save()

    def test_total_distinct_donors(self):
        user1 = RevolvUserProfile.objects.get(id=1)
        user2 = RevolvUserProfile.objects.get(id=2)
        user3 = RevolvUserProfile.objects.get(id=3)

        self.assertEquals(Payment.objects.total_distinct_donors(), 0)
        self._create_payment(user1).save()
        self.assertEquals(Payment.objects.total_distinct_donors(), 1)
        self._create_payment(user1).save()
        self._create_payment(user2, instrument_type=self.reinvestment)
        self._create_payment(user2, instrument_type=self.repayment)
        self.assertEquals(Payment.objects.total_distinct_donors(), 1)
        self._create_payment(user2).save()
        self.assertEquals(Payment.objects.total_distinct_donors(), 2)
        self._create_payment(user3).save()
        self.assertEquals(Payment.objects.total_distinct_donors(), 3)

    def test_payments(self):
        user1 = RevolvUserProfile.objects.get(id=1)
        user2 = RevolvUserProfile.objects.get(id=2)

        self._create_payment(user1).save()
        self._create_payment(user1, instrument_type=self.reinvestment).save()
        self._create_payment(user1, instrument_type=self.repayment).save()

        self._create_payment(user2).save()
        self._create_payment(user2, instrument_type=self.repayment).save()

        self.assertEquals(Payment.objects.payments(user1).count(), 3)
        self.assertEquals(Payment.objects.payments(user2).count(), 2)

    def test_donations(self):
        user1 = RevolvUserProfile.objects.get(id=1)
        user2 = RevolvUserProfile.objects.get(id=2)
        project2 = Project.objects.get(id=2)

        self._create_payment(user1).save()
        self._create_payment(user1, instrument_type=self.reinvestment).save()
        self._create_payment(user1, instrument_type=self.repayment).save()

        self._create_payment(user2, instrument_type=self.repayment).save()

        self.assertEquals(Payment.objects.donations(user1).count(), 1)
        self.assertEquals(Payment.objects.donations(user1, project2).count(), 0)

        self._create_payment(user1, project2).save()
        self.assertEquals(Payment.objects.donations(user1, project2).count(), 1)

        self.assertEquals(Payment.objects.donations(user2).count(), 0)

    def test_reinvestments(self):
        user1 = RevolvUserProfile.objects.get(id=1)
        user2 = RevolvUserProfile.objects.get(id=2)

        self._create_payment(user1).save()
        self._create_payment(user1, instrument_type=self.reinvestment).save()
        self._create_payment(user1, instrument_type=self.repayment).save()

        self._create_payment(user2, instrument_type=self.repayment).save()

        self.assertEquals(Payment.objects.reinvestments(user1).count(), 1)
        self.assertEquals(Payment.objects.reinvestments(user2).count(), 0)

    def test_repayments(self):
        user1 = RevolvUserProfile.objects.get(id=1)
        user2 = RevolvUserProfile.objects.get(id=2)
        project = Project.objects.get(id=1)
        project2 = Project.objects.get(id=2)

        self._create_payment(user1, project=project).save()
        self._create_payment(user1, instrument_type=self.reinvestment, project=project).save()
        self._create_payment(user1, instrument_type=self.repayment, project=project).save()

        self._create_payment(user2, instrument_type=self.repayment, project=project).save()

        self.assertEquals(Payment.objects.repayments(user1).count(), 1)
        self.assertEquals(Payment.objects.repayments(user2).count(), 1)
        self.assertEquals(Payment.objects.repayments(user1, project2).count(), 0)

        self._create_payment(user1, project2, instrument_type=self.repayment).save()
        self.assertEquals(Payment.objects.repayments(user1, project2).count(), 1)
