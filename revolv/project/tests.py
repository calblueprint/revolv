import datetime

from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from django_facebook.utils import get_user_model
from models import Project
from revolv.base.signals import create_profile_of_user
from revolv.payments.models import (Donation, PaymentInstrumentType,
                                    PaymentTransaction)


# Create your tests here.


class ProjectTests(TestCase):
    """Project model tests."""

    def _create_test_project(self,
                             funding_goal=50.0,
                             title="Hello",
                             video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
                             impact_power=50.5,
                             location="Berkeley",
                             end_date=None,
                             mission_statement="We do solar!",
                             cover_photo="http://i.imgur.com/2zMTZgi.jpg",
                             org_start_date=None,
                             actual_energy=25.5,
                             amount_repaid=29.25,
                             ambassador_id=1
                             ):
        """
        Create and return a dummy project for the purposes of testing. Each
        kwarg of this function represents a default value, which can be changed
        if the value matters for the test, or left alone if not relevant. This
        allows test projects with different settings to be created easily based
        on what is being tested.
        """
        if end_date is None:
            end_date = datetime.date.today() - datetime.timedelta(days=1)  # tomorrow
        if org_start_date is None:
            org_start_date = datetime.date.today() + datetime.timedelta(days=1)  # today
        return Project.objects.create(
            funding_goal=funding_goal,
            title=title,
            video_url=video_url,
            impact_power=impact_power,
            location=location,
            end_date=end_date,
            mission_statement=mission_statement,
            cover_photo=cover_photo,
            org_start_date=org_start_date,
            actual_energy=actual_energy,
            amount_repaid=amount_repaid,
            ambassador_id=ambassador_id,
        )

    def _create_test_donation_for_project(self, project, amount):
        """
        Create a donation to the given project of the given amount, made by a
        dummy user via paypal.

        :return: the donation, the transaction, and the user
        """
        user, is_new = User.objects.get_or_create(
            username="aggregateDonationsTestUser",
            email="john@example.com",
            password="permission_test_user_password"
        )
        transaction = PaymentTransaction.objects.create(
            amount=amount,
            payment_instrument_type=PaymentInstrumentType.objects.get_paypal(),
            user=user
        )
        donation = Donation.objects.create(
            payment_transaction=transaction,
            project=project
        )
        return donation, transaction, user

    def test_construct(self):
        self._create_test_project()
        testProject = Project.objects.get(title="Hello")
        self.assertEqual(testProject.mission_statement, "We do solar!")
        self.assertEqual(testProject.impact_power, 50.5)

    def test_save_and_query(self):
        p = self._create_test_project(
            funding_goal=20.0,
            location="San Francisco",
            mission_statement="Blueprint!"
        )
        p.save()
        entry = Project.objects.all().filter(location="San Francisco")[0]
        self.assertEqual(entry.mission_statement, "Blueprint!")

    def test_aggregate_donations(self):
        """Test that project.amount_donated works."""
        project = self._create_test_project()
        self.assertEqual(project.amount_donated, 0.0)
        self._create_test_donation_for_project(project, 50.0)
        self.assertEqual(project.amount_donated, 50.0)
        self._create_test_donation_for_project(project, 25.0)
        self.assertEqual(project.amount_donated, 75.0)

    def test_partial_completeness(self):
        """Test that project.partial_completeness works."""
        project = self._create_test_project(funding_goal=100.0)
        self.assertEqual(project.partial_completeness, 0.0)
        self.assertEqual(project.partial_completeness_as_js(), "0.0")
        self._create_test_donation_for_project(project, 50.0)
        self.assertEqual(project.partial_completeness, 0.5)
        self._create_test_donation_for_project(project, 25.0)
        self.assertEqual(project.partial_completeness, 0.75)
        self.assertEqual(project.partial_completeness_as_js(), "0.75")
        self._create_test_donation_for_project(project, 25.0)
        self.assertEqual(project.partial_completeness, 1.0)
        self.assertEqual(project.partial_completeness_as_js(), "1.0")
        self._create_test_donation_for_project(project, 25.0)
        self.assertEqual(project.partial_completeness, 1.0)


class ProjectManagerTests(TestCase):
    """Tests for the Project manager"""

    def setUp(self):
        post_save.disconnect(receiver=create_profile_of_user, sender=get_user_model())
        call_command('loaddata', 'user', 'revolvuserprofile', 'donation', 'payment_transaction', 'project')

    def tearDown(self):
        post_save.connect(create_profile_of_user, sender=get_user_model())

    def test_get_featured(self):
        context = Project.objects.get_featured(1)
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "The Community Dance Studio")
        context = Project.objects.get_featured(10)
        self.assertEqual(len(context), 2)
        self.assertEqual(context[1].org_name, "Comoonity Dairy")

    def test_get_completed(self):
        context = Project.objects.get_completed()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Comoonity Dairy")

    def test_get_active(self):
        context = Project.objects.get_active()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "The Community Dance Studio")

    def test_get_proposed(self):
        context = Project.objects.get_proposed()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Educathing")

    def test_get_drafted(self):
        context = Project.objects.get_drafted()
        self.assertEqual(len(context), 1)
        self.assertEqual(context[0].org_name, "Fire Emblem")
