import factory
from django.db.models import signals, Sum
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType, RepaymentFragment)
from revolv.payments.utils import (NotEnoughFundingException,
                                   ProjectNotCompleteException)
from revolv.project.models import Category, Project


class PaymentTest(TestCase):
    reinvestment = PaymentType.objects.get_reinvestment_fragment()

    def _create_payment(self, user=None, amount=10.00, project=None, payment_type=None, entrant=None):
        if project is None:
            project = Project.factories.base.create()
        if payment_type is None:
            payment_type = PaymentType.objects.get_paypal()
        if entrant is None:
            entrant = user
        return Payment(amount=amount, user=user, entrant=entrant,
                       payment_type=payment_type, project=project)

    def _create_admin_repayment(self, admin, amount=10.00, project=None):
        if project is None:
            project = Project.factories.base.create()
        return AdminRepayment(amount=amount, admin=admin, project=project)

    def _create_admin_reinvestment(self, admin, amount, project=None):
        if project is None:
            project = Project.factories.base.create()
        return AdminReinvestment(amount=amount, admin=admin, project=project)

    def test_payment_create(self):
        """
        Verify that the payment can be created.
        """
        user = RevolvUserProfile.factories.base.create()
        Payment.factories.base.create(user=user, entrant=user)

    @factory.django.mute_signals(signals.pre_init, signals.post_save)
    def test_total_distinct_organic_donors(self):
        """
        Verify that we can correctly get the total number of distinct organic
        donors to any project.
        """
        user1, user2, user3, admin = RevolvUserProfile.factories.base.create_batch(4)

        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 0)
        self._create_payment(user1).save()
        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 1)

        self._create_payment(user1).save()
        self._create_admin_reinvestment(admin, 100.00).save()
        self._create_admin_repayment(admin).save()

        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 1)

        self._create_payment(user2).save()
        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 2)
        self._create_payment(user3).save()
        self.assertEquals(Payment.objects.total_distinct_organic_donors(), 3)

    def test_payments(self):
        """
        Verify that we can create payments of any type and associate them to
        users.
        """
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)

        self._create_payment(user1).save()
        self._create_payment(user1, payment_type=self.reinvestment).save()

        self._create_payment(user2).save()

        self.assertEquals(Payment.objects.payments(user1).count(), 2)
        self.assertEquals(Payment.objects.payments(user2).count(), 1)

    def test_donations(self):
        """
        Test that we can bookkeep organic donation information.
        """
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        project2 = Project.factories.base.create()

        self._create_payment(user1).save()
        self._create_payment(user1, payment_type=self.reinvestment).save()

        self.assertEquals(Payment.objects.donations(user1).count(), 1)
        self.assertEquals(Payment.objects.donations(user1, project2).count(), 0)

        self._create_payment(user1, project=project2).save()
        self.assertEquals(Payment.objects.donations(user1, project2).count(), 1)

        self.assertEquals(Payment.objects.donations(user2).count(), 0)

    def test_check(self):
        """
        Test that checks work and that they don't affect
        repayments/reinvestments.
        """
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        admin = RevolvUserProfile.factories.admin.create()
        project1, project2 = Project.factories.base.create_batch(2)

        self._create_payment(user=user1,
                             amount=1000.00,
                             project=project1,
                             payment_type=PaymentType.objects.get_check(),
                             entrant=admin).save()

        self._create_payment(user=user2,
                             amount=2000.00,
                             project=project1,
                             payment_type=PaymentType.objects.get_check(),
                             entrant=admin).save()

        self._create_payment(amount=3000.00,
                             project=project1,
                             payment_type=PaymentType.objects.get_check(),
                             entrant=admin).save()

        self.assertEquals(Payment.objects.donations(project=project1,
                                                    organic=True).count(), 0)
        self.assertEquals(project1.get_organic_donations().count(), 0)
        self.assertEquals(project1.amount_donated_organically, 0)
        self.assertEquals(project1.amount_donated, 6000.0)
        self.assertEquals(Payment.objects.donations(project=project1).count(), 3)

        self._create_payment(user=user1,
                             amount=30.00,
                             project=project1,
                             ).save()
        self._create_payment(user=user2,
                             amount=10.00,
                             project=project1,
                             ).save()
        self.assertEquals(Payment.objects.donations(project=project1,
                                                    organic=True).count(), 2)
        self.assertEquals(project1.get_organic_donations().count(), 2)
        self.assertEquals(project1.amount_donated_organically, 40.0)
        self.assertEquals(project1.amount_donated, 6040.0)
        self.assertEquals(Payment.objects.donations(project=project1).count(), 5)

        project1.complete_project()
        self._create_admin_repayment(admin, 100.00, project1).save()
        self.assertEquals(user1.repaymentfragment_set.count(), 1)
        self.assertEquals(user2.repaymentfragment_set.count(), 1)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 75.00)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user2).aggregate(
            Sum('amount')
        )['amount__sum'], 25.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 75.00)
        self.assertEquals(user2.reinvest_pool, 25.00)

        self._create_admin_reinvestment(admin, 100.00, project2).save()
        self.assertEquals(RepaymentFragment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 75.00)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user2).aggregate(
            Sum('amount')
        )['amount__sum'], 25.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 0.0)
        self.assertEquals(user2.reinvest_pool, 0.0)
        self.assertEquals(project2.amount_donated_organically, 0)
        self.assertEquals(project2.amount_donated, 100.0)

        self._create_payment(user=user1,
                             amount=1000.00,
                             project=project2,
                             payment_type=PaymentType.objects.get_check(),
                             entrant=admin).save()
        self.assertEquals(project2.amount_donated_organically, 0)
        self.assertEquals(project2.amount_donated, 1100.0)

    def test_proportion_donated(self):
        """
        Verify that donation proportions are calculated correctly.
        For user U, project P the proportion that a user has donated is:

            Sum of U's donations to P / Total organic donation amount to P
        """
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        admin1 = RevolvUserProfile.factories.admin.create()
        project = Project.factories.base.create()

        self.assertEquals(Payment.objects.donations(project=project).count(), 0)

        self._create_payment(user1, 30.00, project).save()
        self.assertEquals(Payment.objects.donations(project=project).count(), 1)
        self.assertEquals(project.proportion_donated(user1), 1.0)

        self._create_payment(user2, 10.00, project).save()
        self.assertEquals(Payment.objects.donations(project=project).count(), 2)
        self.assertEquals(project.proportion_donated(user2), 10.0 / 40.0)
        self.assertEquals(project.proportion_donated(user1), 30.0 / 40.0)

        project.complete_project()  # must complete project before repayment

        self._create_admin_repayment(admin1, 100.00, project).save()
        self._create_admin_reinvestment(admin1, 100.00, project).save()
        self.assertEquals(Payment.objects.donations(project=project).count(), 2)
        self.assertEquals(project.proportion_donated(user2), 10.0 / 40.0)
        self.assertEquals(project.proportion_donated(user1), 30.0 / 40.0)

    def test_bad_repayment(self):
        """
        Test that we can't make a repayment on a not-completed project.
        """
        project = Project.factories.base.create()
        admin = RevolvUserProfile.factories.admin.create()
        self.assertRaises(ProjectNotCompleteException,
                          self._create_admin_repayment,
                          admin, 100.00, project  # *args
                          )

    def test_repayment_multiple_save(self):
        """
        Test that saving a repayment multiple times does not generate
        extra RepaymentFragments
        """
        user = RevolvUserProfile.factories.base.create()
        admin = RevolvUserProfile.factories.admin.create()
        project = Project.factories.base.create()
        self._create_payment(user, project=project).save()
        project.complete_project()

        repay = self._create_admin_repayment(admin, 100.00, project)
        repay.save()
        self.assertEquals(user.repaymentfragment_set.filter(
            project=project
        ).count(), 1)

        repay.save()
        self.assertEquals(user.repaymentfragment_set.filter(
            project=project
        ).count(), 1)

    def test_bad_reinvestment(self):
        """
        Test that we can't make a reinvestment if we have insufficient
        funds.
        """
        user = RevolvUserProfile.factories.base.create()
        admin = RevolvUserProfile.factories.admin.create()
        project = Project.factories.base.create()
        self._create_payment(user, project=project).save()
        project.complete_project()

        self._create_admin_repayment(admin, 100.00, project).save()
        self.assertRaises(NotEnoughFundingException,
                          self._create_admin_reinvestment,
                          admin, 200.00, project  # *args
                          )

    def test_reinvestment_multiple_save(self):
        """
        Test that saving a reinvestment multiple times does not generate
        extra 'reinvestment_fragment'-type Payments
        """
        user = RevolvUserProfile.factories.base.create()
        admin = RevolvUserProfile.factories.admin.create()
        project1, project2 = Project.factories.base.create_batch(2)
        self._create_payment(user, project=project1).save()
        project1.complete_project()

        self._create_admin_repayment(admin, 100.00, project1).save()
        reinvest1 = self._create_admin_reinvestment(admin, 100.00, project=project2)

        reinvest1.save()
        self.assertEquals(Payment.objects.reinvestment_fragments(user).count(), 1)

        reinvest1.save()
        self.assertEquals(Payment.objects.reinvestment_fragments(user).count(), 1)

    def test_repayment(self):
        """
        Test repayment bookkeeping. Lots of moving parts and relations,
        see docstrings for respective models for info.
        """
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        admin1, admin2 = RevolvUserProfile.factories.admin.create_batch(2)
        project1, project2 = Project.factories.base.create_batch(2)

        self._create_payment(user1, amount=10.00, project=project1).save()
        self._create_payment(user2, amount=30.00, project=project1).save()
        project1.complete_project()

        repay1 = self._create_admin_repayment(admin1, amount=100.00, project=project1)
        repay1.save()

        self.assertEquals(user1.repaymentfragment_set.count(), 1)
        self.assertEquals(user2.repaymentfragment_set.count(), 1)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 25.00)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user2).aggregate(
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

        self.assertEquals(user1.repaymentfragment_set.count(), 2)
        self.assertEquals(user2.repaymentfragment_set.count(), 2)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user1, project=project2).aggregate(
            Sum('amount')
        )['amount__sum'], 150.00)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user2, project=project2).aggregate(
            Sum('amount')
        )['amount__sum'], 50.00)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 175.00)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user2).aggregate(
            Sum('amount')
        )['amount__sum'], 125.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 175.00)
        self.assertEquals(user2.reinvest_pool, 125.00)

        repay1.delete()

        self.assertEquals(user1.repaymentfragment_set.filter(project=project1).count(), 0)
        self.assertEquals(user2.repaymentfragment_set.filter(project=project1).count(), 0)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user1).aggregate(
            Sum('amount')
        )['amount__sum'], 150.00)
        self.assertEquals(RepaymentFragment.objects.repayments(user=user2).aggregate(
            Sum('amount')
        )['amount__sum'], 50.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 150.00)
        self.assertEquals(user2.reinvest_pool, 50.00)

    def test_user_reinvestment(self):
        """
        Test reinvestment on single Payment level.
        """
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)

        self._create_payment(user1).save()
        self._create_payment(user1, payment_type=self.reinvestment).save()
        self._create_payment(user1).save()

        self._create_payment(user2).save()

        self.assertEquals(Payment.objects.reinvestment_fragments(user1).count(), 1)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2).count(), 0)

    def test_admin_reinvestment(self):
        """
        Test reinvestment on AdminReinvestment level. Lots of moving parts,
        see docstrings for respective models for info.
        """
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        admin1 = RevolvUserProfile.factories.admin.create()
        project1, project2 = Project.factories.base.create_batch(2)

        self._create_payment(user1, amount=25.00, project=project1).save()
        self._create_payment(user2, amount=75.00, project=project1).save()
        project1.complete_project()
        self._create_admin_repayment(admin1, amount=200.00, project=project1).save()

        reinvest1 = self._create_admin_reinvestment(admin1, 200.00, project=project2)
        reinvest1.save()

        self.assertEquals(project2.amount_donated, 200.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1, project2), 50.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2, project2), 150.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 0)
        self.assertEquals(user2.reinvest_pool, 0)

        reinvest1.delete()

        self.assertEquals(project2.amount_donated, 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2), 0)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)

    def test_admin_reinvestment_category_preference(self):
        """
        Test reinvestment on AdminReinvestment level. Lots of moving parts,
        see docstrings for respective models for info.

        Creates 3 users, 2 of which have category preferences that match categories
        for project2. Creates a reinvestment equal to the sum of the pools for
        the two users with preferences. Checks that those 2 users will reinvest into
        it completely, and that the other users do not.
        """
        user1, user2, user3 = RevolvUserProfile.factories.base.create_batch(3)
        admin1 = RevolvUserProfile.factories.admin.create()
        project1 = Project.factories.base.create(funding_goal=200)
        project2 = Project.factories.base.create(funding_goal=250)

        category1, category2, category3 = Category.factories.base.create_batch(3)

        # assigns preferred categories for users and categories for project
        user1.preferred_categories.add(category2)
        user2.preferred_categories.add(category3)
        user3.preferred_categories.add(category1, category3)
        project2.category_set.add(category1, category2)

        self._create_payment(user1, amount=25.00, project=project1).save()
        self._create_payment(user2, amount=75.00, project=project1).save()
        self._create_payment(user3, amount=100.00, project=project1).save()
        project1.complete_project()

        self._create_admin_repayment(admin1, amount=400.00, project=project1).save()

        # verifies that reinvestment pools have values that we expect, must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)

        reinvest1 = self._create_admin_reinvestment(admin1, 250.00, project=project2)
        reinvest1.save()

        # checks that only users with preferences for project 2 actually donate
        self.assertEquals(project2.amount_donated, 250.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1, project2), 50.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2, project2).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2, project2), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3, project2), 200.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 0)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 0)

        reinvest1.delete()

        # checks that after deleting, we have no reinvestment fragments
        self.assertEquals(project2.amount_donated, 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3), 0)

        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)

    def test_admin_reinvestment_leftover_reinvest_pool(self):
        """
        Test reinvestment on AdminReinvestment level. Lots of moving parts,
        see docstrings for respective models for info.

        Creates 3 users, 2 of which have category preferences that match
        categories for project2. Creates a reinvestment large enough to exhaust
        the pools of users with preferences, and use some from the user without
        preferences. Checks that those 2 users will reinvest into
        it completely, and that the other user will invest the remainder and
        have leftover funds after the project hits its reinvestment goal.
        """
        user1, user2, user3 = RevolvUserProfile.factories.base.create_batch(3)
        admin1 = RevolvUserProfile.factories.admin.create()
        project1 = Project.factories.base.create(funding_goal=200)
        project2 = Project.factories.base.create(funding_goal=350)

        category1, category2, category3 = Category.factories.base.create_batch(3)

        # assigns preferred categories for users and categories for project
        user1.preferred_categories.add(category2)
        user2.preferred_categories.add(category3)
        user3.preferred_categories.add(category1, category3)
        project2.category_set.add(category1, category2)

        self._create_payment(user1, amount=25.00, project=project1).save()
        self._create_payment(user2, amount=75.00, project=project1).save()
        self._create_payment(user3, amount=100.00, project=project1).save()
        project1.complete_project()

        self._create_admin_repayment(admin1, amount=400.00, project=project1).save()

        # verifies that reinvestment pools have values that we expect, must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)

        reinvest1 = self._create_admin_reinvestment(admin1, 350.00, project=project2)
        reinvest1.save()

        # checks that all three users donate, and user 2, the user with no preferences,
        # has leftover funds
        self.assertEquals(project2.amount_donated, 350.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1, project2), 50.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2, project2), 100.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3, project2), 200.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 0)
        self.assertEquals(user2.reinvest_pool, 50.00)
        self.assertEquals(user3.reinvest_pool, 0)

        reinvest1.delete()

        # checks that after deleting, we have no reinvestment fragments
        self.assertEquals(project2.amount_donated, 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3), 0)

        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)

    def test_admin_reinvestment_depleted_reinvestment_pool(self):
        """
        Test reinvestment on AdminReinvestment level. Lots of moving parts,
        see docstrings for respective models for info.

        Creates 3 users, 1 of which have category preferences that match
        categories for project2. Creates a reinvestment equal to the sum of all
        the user's reinvestment pools. Checks that all three users will exhaust their
        reinvest pools.
        """
        user1, user2, user3 = RevolvUserProfile.factories.base.create_batch(3)
        admin1 = RevolvUserProfile.factories.admin.create()
        project1 = Project.factories.base.create(funding_goal=200)
        project2 = Project.factories.base.create(funding_goal=450)

        category1, category2, category3 = Category.factories.base.create_batch(3)

        # assigns preferred categories for users and categories for project
        user1.preferred_categories.add(category2)
        user2.preferred_categories.add(category3)
        project2.category_set.add(category1, category2)

        self._create_payment(user1, amount=25.00, project=project1).save()
        self._create_payment(user2, amount=75.00, project=project1).save()
        self._create_payment(user3, amount=100.00, project=project1).save()
        project1.complete_project()

        self._create_admin_repayment(admin1, amount=400.00, project=project1).save()

        # verifies that reinvestment pools have values that we expect, must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)

        reinvest1 = self._create_admin_reinvestment(admin1, 400.00, project=project2)
        reinvest1.save()

        # checks that all three users donate, and that all of their reinvest pools are depleted
        self.assertEquals(project2.amount_donated, 400.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1, project2), 50.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2, project2), 150.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3, project2), 200.00)

        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 0)
        self.assertEquals(user2.reinvest_pool, 0)
        self.assertEquals(user3.reinvest_pool, 0)

        reinvest1.delete()

        # checks that after deleting, we have no reinvestment fragments
        self.assertEquals(project2.amount_donated, 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3), 0)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)

    def test_admin_multiple_reinvestments(self):
        """
        Test reinvestment on AdminReinvestment level. Lots of moving parts,
        see docstrings for respective models for info.

        Creates 3 users, 1 of which have category preferences that match
        categories for project2. Creates a reinvestment equal to the sum of all
        the user's reinvestment pools. Checks that all three users will exhaust their
        reinvest pools.
        """
        user1, user2, user3 = RevolvUserProfile.factories.base.create_batch(3)
        admin1 = RevolvUserProfile.factories.admin.create()
        project1 = Project.factories.base.create(funding_goal=200)
        project2 = Project.factories.base.create(funding_goal=250)
        project3 = Project.factories.base.create(funding_goal=450)

        category1, category2, category3 = Category.factories.base.create_batch(3)

        # assigns preferred categories for users and categories for project
        user1.preferred_categories.add(category1)
        user2.preferred_categories.add(category2)
        user3.preferred_categories.add(category3)
        project2.category_set.add(category1, category3)

        self._create_payment(user1, amount=25.00, project=project1).save()
        self._create_payment(user2, amount=75.00, project=project1).save()
        self._create_payment(user3, amount=100.00, project=project1).save()
        project1.complete_project()

        self._create_admin_repayment(admin1, amount=400.00, project=project1).save()

        # verifies that reinvestment pools have values that we expect, must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)

        reinvest1 = self._create_admin_reinvestment(admin1, 250.00, project=project2)
        reinvest1.save()

        # checks that user 1 and user 3 donate
        self.assertEquals(project2.amount_donated, 250.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1, project2), 50.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2, project2).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2, project2), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3, project2).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3, project2), 200.00)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 0)
        self.assertEquals(user2.reinvest_pool, 150)
        self.assertEquals(user3.reinvest_pool, 0)

        reinvest2 = self._create_admin_reinvestment(admin1, 150.00, project=project3)
        reinvest2.save()

        # checks that user 1 and user 3 donate
        self.assertEquals(project3.amount_donated, 150.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1, project3).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1, project3), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2, project3).count(), 1)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2, project3), 150.00)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3, project3).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3, project3), 0)
        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 0)
        self.assertEquals(user2.reinvest_pool, 0)
        self.assertEquals(user3.reinvest_pool, 0)

        reinvest1.delete()
        reinvest2.delete()

        # checks that after deleting, we have no reinvestment fragments
        self.assertEquals(project2.amount_donated, 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user1).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user1), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user2).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user2), 0)
        self.assertEquals(Payment.objects.reinvestment_fragments(user3).count(), 0)
        self.assertEquals(Payment.objects.total_reinvestment_amount(user3), 0)

        # must reload to get new reinvest_pool amount
        user1 = RevolvUserProfile.objects.get(pk=user1.pk)
        user2 = RevolvUserProfile.objects.get(pk=user2.pk)
        user3 = RevolvUserProfile.objects.get(pk=user3.pk)
        self.assertEquals(user1.reinvest_pool, 50.00)
        self.assertEquals(user2.reinvest_pool, 150.00)
        self.assertEquals(user3.reinvest_pool, 200.00)
