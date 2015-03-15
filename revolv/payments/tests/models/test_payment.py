from django.db.models import Sum
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType, Repayment)
from revolv.project.models import Project


class PaymentTest(TestCase):
    reinvestment = PaymentType.objects.get_reinvestment()

    def _create_payment(self, user, amount=10.00, project=None, payment_type=None):
        if project is None:
            project = Project.factories.base.create()
        if payment_type is None:
            payment_type = PaymentType.objects.get_paypal()
        return Payment(amount=amount, user=user, entrant=user, payment_type=payment_type, project=project)

    def _create_admin_repayment(self, admin, amount=10.00, project=None):
        if project is None:
            project = Project.factories.base.create()
        return AdminRepayment(amount=amount, admin=admin, project=project)

    def _create_admin_reinvestment(self, admin, amount, project=None, test_obj=False):
        if project is None:
            project = Project.factories.base.create()
        return AdminReinvestment(amount=amount, admin=admin, project=project, test_obj=test_obj)

    def test_payment_create(self):
        """Verify that the payment can be created."""
        user = RevolvUserProfile.factories.base.create()
        Payment.factories.base.create(user=user, entrant=user)

    def test_total_distinct_organic_donors(self):
        """Verify that we can correctly get the total number of distinct donors to any project."""
        user1, user2, user3, admin = RevolvUserProfile.factories.base.create_batch(4)

        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 0)
        self._create_payment(user1).save()
        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 1)

        self._create_payment(user1).save()
        self._create_admin_reinvestment(admin, 100.00, test_obj=True).save()
        self._create_admin_repayment(admin).save()

        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 1)

        self._create_payment(user2).save()
        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 2)
        self._create_payment(user3).save()
        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 3)

    def test_payments(self):
        """Verify that we can create payments of any type and associate them to users."""
        user1, user2, admin = RevolvUserProfile.factories.base.create_batch(3)

        self._create_payment(user1).save()
        self._create_payment(user1, payment_type=self.reinvestment).save()

        self._create_payment(user2).save()

        self.assertEquals(Payment.objects.payments(user1).count(), 2)
        self.assertEquals(Payment.objects.payments(user2).count(), 1)

    def test_donations(self):
        """Test that we can bookkeep organic donation information."""
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        project2 = Project.factories.base.create()

        self._create_payment(user1).save()
        self._create_payment(user1, payment_type=self.reinvestment).save()

        self.assertEquals(Payment.objects.donations(user1).count(), 1)
        self.assertEquals(Payment.objects.donations(user1, project2).count(), 0)

        self._create_payment(user1, project=project2).save()
        self.assertEquals(Payment.objects.donations(user1, project2).count(), 1)

        self.assertEquals(Payment.objects.donations(user2).count(), 0)

    def test_proportion_donated(self):
        """Verify that repayment proportions are correct."""
        user1, user2, admin1 = RevolvUserProfile.factories.base.create_batch(3)
        project = Project.factories.base.create()

        self.assertEquals(Payment.objects.donations(project=project).count(), 0)

        self._create_payment(user1, 30.00, project).save()
        self.assertEquals(Payment.objects.donations(project=project).count(), 1)
        self.assertEquals(project.proportion_donated(user1), 1.0)

        self._create_payment(user2, 10.00, project).save()
        self.assertEquals(Payment.objects.donations(project=project).count(), 2)
        self.assertEquals(project.proportion_donated(user2), 10.0 / 40.0)
        self.assertEquals(project.proportion_donated(user1), 30.0 / 40.0)

        self._create_admin_repayment(admin1, 100.00, project).save()
        self._create_admin_reinvestment(admin1, 100.00, project).save()
        self.assertEquals(Payment.objects.donations(project=project).count(), 2)
        self.assertEquals(project.proportion_donated(user2), 10.0 / 40.0)
        self.assertEquals(project.proportion_donated(user1), 30.0 / 40.0)

    def test_repayment(self):
        """Test repayment bookkeeping."""
        admin1, admin2 = RevolvUserProfile.factories.base.create_batch(2)
        admin1.make_administrator()
        admin2.make_administrator()

        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        project1, project2 = Project.factories.base.create_batch(2)

        self._create_payment(user1, amount=10.00, project=project1).save()
        self._create_payment(user2, amount=30.00, project=project1).save()
        project1.complete_project()

        repay1 = self._create_admin_repayment(admin1, amount=100.00, project=project1)
        repay1.save()
        self.assertEquals(user1.repayment_set.count(), 1)
        self.assertEquals(user2.repayment_set.count(), 1)
        self.assertEquals(Repayment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 25.00)
        self.assertEquals(Repayment.objects.repayments(user=user2).aggregate(
            Sum('amount')
        )['amount__sum'], 75.00)
        # TODO: is it a good idea to cache this?
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 25.00)
        self.assertEquals(user2.reinvest_pool, 75.00)

        self._create_payment(user1, amount=30.00, project=project2).save()
        self._create_payment(user2, amount=10.00, project=project2).save()
        project2.complete_project()

        self._create_admin_repayment(admin2, amount=200.00, project=project2).save()
        self.assertEquals(user1.repayment_set.count(), 2)
        self.assertEquals(user2.repayment_set.count(), 2)
        self.assertEquals(Repayment.objects.repayments(user=user1, project=project2).aggregate(
            Sum('amount')
        )['amount__sum'], 150.00)
        self.assertEquals(Repayment.objects.repayments(user=user2, project=project2).aggregate(
            Sum('amount')
        )['amount__sum'], 50.00)
        self.assertEquals(Repayment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 175.00)
        self.assertEquals(Repayment.objects.repayments(user=user2).aggregate(
            Sum('amount')
        )['amount__sum'], 125.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 175.00)
        self.assertEquals(user2.reinvest_pool, 125.00)

        repay1.delete()
        self.assertEquals(user1.repayment_set.filter(project=project1).count(), 0)
        self.assertEquals(user2.repayment_set.filter(project=project1).count(), 0)
        self.assertEquals(Repayment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 150.00)
        self.assertEquals(Repayment.objects.repayments(user=user2).aggregate(
            Sum('amount')
        )['amount__sum'], 50.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 150.00)
        self.assertEquals(user2.reinvest_pool, 50.00)

    # def test_reinvestments(self):
    #     """Test that we can bookkeep reinvestment information."""
    #     user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
    #
    #     self._create_payment(user1).save()
    #     self._create_payment(user1, payment_type=self.reinvestment).save()
    #     self._create_payment(user1).save()
    #
    #     self._create_payment(user2).save()
    #
    #     self.assertEquals(Payment.objects.reinvestments(user1).count(), 1)
    #     self.assertEquals(Payment.objects.reinvestments(user2).count(), 0)
