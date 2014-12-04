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

    def _create_test_project(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        return Project.objects.create(
            funding_goal=50.0,
            title="Hello",
            video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
            impact_power=50.5,
            location="Berkeley",
            end_date=tomorrow,
            mission_statement="We do solar!",
            cover_photo="http://i.imgur.com/2zMTZgi.jpg",
            org_start_date=yesterday,
            actual_energy=25.5,
            amount_repaid=29.25,
            ambassador_id=1,
        )

    def test_construct(self):
        self._create_test_project()
        testProject = Project.objects.get(title="Hello")
        self.assertEqual(testProject.mission_statement, "We do solar!")
        self.assertEqual(testProject.impact_power, 50.5)

    def test_save_and_query(self):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        p = Project(
            funding_goal=20.0,
            title="Hello",
            video_url="https://www.youtube.com/watch?v=9bZkp7q19f0",
            impact_power=50.5,
            location="San Francisco",
            end_date=tomorrow,
            mission_statement="Blueprint!",
            cover_photo="http://i.imgur.com/2zMTZgi.jpg",
            org_start_date=yesterday,
            actual_energy=25.5,
            amount_repaid=29.25,
            ambassador_id=1,
        )
        p.save()
        entry = Project.objects.all().filter(location="San Francisco")[0]
        self.assertEqual(entry.mission_statement, "Blueprint!")

    def test_aggregate_donations(self):
        user = User.objects.create_user(
            "aggregateDonationsTestUser",
            "john@example.com",
            "permission_test_user_password"
        )
        project = self._create_test_project()
        transaction1 = PaymentTransaction.objects.create(
            amount=50.0,
            payment_instrument_type=PaymentInstrumentType.objects.get_paypal(),
            user=user
        )
        Donation.objects.create(
            payment_transaction=transaction1,
            project=project
        )
        self.assertEqual(project.amount_donated, 50.0)
        transaction2 = PaymentTransaction.objects.create(
            amount=25.0,
            payment_instrument_type=PaymentInstrumentType.objects.get_paypal(),
            user=user
        )
        Donation.objects.create(
            payment_transaction=transaction2,
            project=project
        )
        self.assertEqual(project.amount_donated, 75.0)


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
