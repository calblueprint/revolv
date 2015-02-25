import datetime
import json

from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from django_facebook.utils import get_user_model
from revolv.base.models import RevolvUserProfile
from revolv.base.signals import create_profile_of_user
from revolv.base.tests.tests import TestUserMixin
from revolv.payments.models import Payment, PaymentInstrumentType
from revolv.project.models import Project
from revolv.project.tasks import scrape


# Create your tests here.
class CreateTestProjectMixin(object):
    def create_test_project(self,
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

    def create_test_donation_for_project(self, project, amount):
        """
        Create a payment to the given project of the given amount, made by a
        dummy user via paypal.

        :return: the payment and the user
        """
        user = RevolvUserProfile.objects.get(id=1)
        payment = Payment.objects.create(
            amount=amount,
            payment_instrument_type=PaymentInstrumentType.objects.get_paypal(),
            user=user,
            entrant=user,
            project=project
        )
        return payment, user

    def create_test_repayment_for_project(self, project, amount):
        """
        Create a repayment to a given project of the given amount, entered by
        a dummy user.

        :return: the repayment and the user
        """
        user1 = RevolvUserProfile.objects.get(id=1)
        user2 = RevolvUserProfile.objects.get(id=2)
        payment = Payment.objects.create(
            amount=amount / 2,
            payment_instrument_type=PaymentInstrumentType.objects.get_repayment(),
            user=user1,
            entrant=user2,
            project=project
        )
        payment = Payment.objects.create(
            amount=amount / 2,
            payment_instrument_type=PaymentInstrumentType.objects.get_repayment(),
            user=user2,
            entrant=user2,
            project=project
        )
        return payment, user1, user2


class ProjectTests(CreateTestProjectMixin, TestCase):
    """Project model tests."""

    def setUp(self):
        post_save.disconnect(receiver=create_profile_of_user, sender=get_user_model())
        call_command('loaddata', 'user', 'revolvuserprofile', 'project')

    def tearDown(self):
        post_save.connect(create_profile_of_user, sender=get_user_model())

    def test_construct(self):
        self.create_test_project()
        testProject = Project.objects.get(title="Hello")
        self.assertEqual(testProject.mission_statement, "We do solar!")
        self.assertEqual(testProject.impact_power, 50.5)

    def test_save_and_query(self):
        p = self.create_test_project(
            funding_goal=20.0,
            location="San Francisco",
            mission_statement="Blueprint!"
        )
        p.save()
        entry = Project.objects.all().filter(location="San Francisco")[0]
        self.assertEqual(entry.mission_statement, "Blueprint!")

    def test_aggregate_donations(self):
        """Test that project.amount_donated works."""
        project = self.create_test_project(funding_goal=200.0)
        self.assertEqual(project.amount_donated, 0.0)
        self.assertEqual(project.amount_left, 200.0)
        self.create_test_donation_for_project(project, 50.0)
        self.assertEqual(project.amount_donated, 50.0)
        self.assertEqual(project.amount_left, 150.0)
        self.create_test_donation_for_project(project, 25.50)
        self.create_test_repayment_for_project(project, 50)
        self.assertEqual(project.amount_donated, 75.50)
        self.assertEqual(project.amount_left, 124.50)
        self.assertEqual(project.rounded_amount_left, 124.00)

    def test_amount_repaid(self):
        project = self.create_test_project(funding_goal=200.0)
        self.assertEqual(project.amount_repaid, 0.0)
        self.create_test_repayment_for_project(project, 50)
        self.assertEqual(project.amount_repaid, 50.0)
        self.create_test_repayment_for_project(project, 60)
        self.assertEqual(project.amount_repaid, 110.0)

    def test_partial_completeness(self):
        """Test that project.partial_completeness works."""
        project = self.create_test_project(funding_goal=100.0)
        self.assertEqual(project.partial_completeness, 0.0)
        self.assertEqual(project.partial_completeness_as_js(), "0.0")
        self.create_test_donation_for_project(project, 50.0)
        self.assertEqual(project.partial_completeness, 0.5)
        self.create_test_donation_for_project(project, 25.0)
        self.assertEqual(project.partial_completeness, 0.75)
        self.assertEqual(project.partial_completeness_as_js(), "0.75")
        self.create_test_donation_for_project(project, 25.0)
        self.assertEqual(project.partial_completeness, 1.0)
        self.assertEqual(project.partial_completeness_as_js(), "1.0")
        self.create_test_donation_for_project(project, 25.0)
        self.assertEqual(project.partial_completeness, 1.0)

    def test_days_remaining(self):
        """
        Test that the functions related to the amount of time remaning in
        the project work correctly.
        """
        project = self.create_test_project(end_date=datetime.date.today() - datetime.timedelta(days=10))
        self.assertEqual(project.days_left, 10)
        self.assertEqual(project.formatted_days_left(), "10 days left")
        project = self.create_test_project(end_date=datetime.date.today() - datetime.timedelta(days=1))
        self.assertEqual(project.days_left, 1)
        self.assertEqual(project.formatted_days_left(), "1 day left")
        project = self.create_test_project(end_date=datetime.date.today() - datetime.timedelta(minutes=10, days=0))
        self.assertEqual(project.days_left, 0)
        self.assertEqual(project.formatted_days_left(), Project.LESS_THAN_ONE_DAY_LEFT_STATEMENT)
        project = self.create_test_project(end_date=datetime.date.today() + datetime.timedelta(days=1))
        self.assertEqual(project.days_left, 0)
        self.assertEqual(project.formatted_days_left(), Project.NO_DAYS_LEFT_STATEMENT)


class ProjectManagerTests(TestCase):
    """Tests for the Project manager"""

    def setUp(self):
        post_save.disconnect(receiver=create_profile_of_user, sender=get_user_model())
        call_command('loaddata', 'user', 'revolvuserprofile', 'payment', 'project')

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


class RequestTest(CreateTestProjectMixin, TestCase):
    """Test that all is well with the project pages."""

    def _assert_project_page_works(self, project):
        resp = self.client.get(project.get_absolute_url())
        self.assertNotEqual(resp.status_code, 500)

    def test_project_page(self):
        project = self.create_test_project()

        for status_choice in Project.PROJECT_STATUS_CHOICES:
            status = status_choice[0]
            project.project_status = status
            project.save()
            self._assert_project_page_works(project)


class ScrapeTest(TestCase):
    """Test that the scrape task runs with no errors,
        and changes the project's solar data files"""

    def test_scrape(self):
        result = scrape.delay()
        self.assertTrue(result.successful())


class DonationAjaxTestCase(CreateTestProjectMixin, TestUserMixin, TestCase):
    """
    Test suite for AJAX payment donations for projects.
    """
    VALIDATE = 'payment/validate'
    SUBMIT = 'payment/submit'

    def setUp(self):
        super(DonationAjaxTestCase, self).setUp()
        self._send_test_user_login_request()
        self.project = self.create_test_project()
        self.project.project_status = Project.ACTIVE
        self.project.save()

    def _make_valid_payment(self):
        """
        Makes valid payment via AJAX to /project/<pk>/payment/validate.
        Returns response from AJAX request.
        """
        valid_payment = {
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value,
            'type': 'visa',
            'first_name': 'William',
            'last_name': 'Taft',
            'expire_month': 6,
            'expire_year': 2020,
            'cvv2': '00',
            'number': '1234123412341234',
            'amount': '10.00',
        }
        resp = self.client.post(
            self.project.get_absolute_url() + self.VALIDATE,
            data=valid_payment,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        return resp

    def test_payment_validation_ajax(self):
        """
        Tests that valid payment validates successfully on /payment/validate
        endpoint.
        """
        resp = self._make_valid_payment()
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIsNone(content.get('error'))

    def test_invalid_payment_ajax(self):
        """
        Tests that invalid payment appropriately errors with on
        /payment/validate endpoint.
        """
        invalid_payment = {
            'csrfmiddlewaretoken': self.client.cookies['csrftoken'].value,
            'type': 'visa',
            # 'first_name': '',
            'last_name': 'Taft',
            'expire_month': 6,
            'expire_year': 2020,
            'cvv2': '00',
            'number': 'not a number',
            'amount': '10.00',
        }
        resp = self.client.post(
            self.project.get_absolute_url() + self.VALIDATE,
            data=invalid_payment,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertIsNotNone(content['error'])

    def test_valid_confirm_ajax(self):
        """
        Tests that valid payment submits successfully on /payment/submit
        endpoint. (Every payment must be validated and then confirmed.)
        """
        confirm = json.loads(self._make_valid_payment().content)['confirm']
        self.assertNotEqual(confirm, {})

        confirm['csrfmiddlewaretoken'] = self.client.cookies['csrftoken'].value
        resp = self.client.post(
            self.project.get_absolute_url() + self.SUBMIT,
            data=confirm,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(resp.status_code, 200)
        content = json.loads(resp.content)

        self.assertEqual(confirm['amount'], content['amount'])

    def test_invalid_confirm_ajax(self):
        """
        Tests that invalid payment appropriately errors on /payment/submit
        endpoint. (Every payment must be validated and then confirmed.)
        """
        confirm = json.loads(self._make_valid_payment().content)['confirm']
        self.assertNotEqual(confirm, {})

        del confirm['amount']
        confirm['csrfmiddlewaretoken'] = self.client.cookies['csrftoken'].value
        resp = self.client.post(
            self.project.get_absolute_url() + self.SUBMIT,
            data=confirm,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertTrue(resp.status_code, 400)
        content = json.loads(resp.content)

        self.assertIsNotNone(content['error'])
