import datetime
import json

import factory
import mock
from django.db.models import signals
from django.test import TestCase
from django_webtest import WebTest
from revolv.base.models import RevolvUserProfile
from revolv.base.tests.tests import TestUserMixin
from revolv.payments.models import (AdminReinvestment, AdminRepayment, Payment,
                                    PaymentType)
from revolv.project.models import Category, Project
from revolv.project.tasks import scrape


class ProjectTests(TestCase):
    """Project model tests."""

    def test_construct(self):
        """Test that we can create a project via factories."""
        test_project = Project.factories.base.build(
            mission_statement="We do solar!",
            impact_power=50.5,
            tagline="Solar is great"
        )
        self.assertEqual(test_project.mission_statement, "We do solar!")
        self.assertEqual(test_project.impact_power, 50.5)
        self.assertEqual(test_project.tagline, "Solar is great")

    def test_save_and_query(self):
        """Test that we can save and then query a project."""
        Project.factories.base.create(
            funding_goal=20.0,
            location="San Francisco",
            mission_statement="Blueprint!",
        )
        entry = Project.objects.all().filter(location="San Francisco")[0]
        self.assertEqual(entry.mission_statement, "Blueprint!")

    @factory.django.mute_signals(signals.pre_init, signals.post_save)
    def test_aggregate_donations(self):
        """Test that project.amount_donated works."""
        project = Project.factories.base.create(funding_goal=200.0, amount_donated=0.0, amount_left=200.0)

        Payment.factories.donation.create(project=project, amount=50.0)
        self.assertEqual(project.amount_donated, 50.0)
        self.assertEqual(project.amount_left, 150.0)

        Payment.factories.donation.create(project=project, amount=25.5)
        AdminReinvestment.factories.base.create(project=project, amount=25.0)
        AdminReinvestment.factories.base.create(project=project, amount=10.0)
        self.assertEqual(project.amount_donated, 110.5)
        self.assertEqual(project.amount_left, 200.0 - 110.5)
        self.assertEqual(project.rounded_amount_left, int(200.0 - 110.5))

    def test_donors_relation(self):
        """
        Make sure that a user isn't removed from the donors relation of a
        project if he has *multiple* donations to that project but only *one* is
        deleted.
        """
        user = RevolvUserProfile.factories.base.create()
        project = Project.factories.base.create()

        payment1 = Payment.factories.base.create(
            user=user,
            entrant=user,
            payment_type=PaymentType.objects.get_paypal(),
            project=project
        )
        self.assertEquals(project.donors.filter(user=user).count(), 1)

        payment2 = Payment.factories.base.create(
            user=user,
            entrant=user,
            payment_type=PaymentType.objects.get_paypal(),
            project=project
        )
        self.assertEquals(project.donors.filter(user=user).count(), 1)

        payment1.delete()
        self.assertEquals(project.donors.filter(user=user).count(), 1)

        payment2.delete()
        self.assertEquals(project.donors.filter(user=user).count(), 0)

    def test_amount_repaid(self):
        """Test that we calculate the amount repaied on a project correctly."""
        project = Project.factories.base.create(funding_goal=200.0)
        self.assertEqual(project.amount_repaid, 0.0)
        project.complete_project()  # must complete project to make repayments
        AdminRepayment.factories.base.create(project=project, amount=50)
        self.assertEqual(project.amount_repaid, 50.0)
        AdminRepayment.factories.base.create(project=project, amount=60)
        self.assertEqual(project.amount_repaid, 110.0)

    def test_partial_completeness(self):
        """Test that project.partial_completeness works."""
        project = Project.factories.base.create(funding_goal=100.0)
        self.assertEqual(project.partial_completeness, 0.0)
        self.assertEqual(project.partial_completeness_as_js(), "0.0")

        Payment.factories.donation.create(project=project, amount=50.0)
        self.assertEqual(project.partial_completeness, 0.5)

        Payment.factories.donation.create(project=project, amount=25.0)
        self.assertEqual(project.partial_completeness, 0.75)
        self.assertEqual(project.partial_completeness_as_js(), "0.75")

        Payment.factories.donation.create(project=project, amount=25.0)
        self.assertEqual(project.partial_completeness, 1.0)
        self.assertEqual(project.partial_completeness_as_js(), "1.0")

        Payment.factories.donation.create(project=project, amount=25.0)
        self.assertEqual(project.partial_completeness, 1.0)

    def test_days_remaining(self):
        """
        Test that the functions related to the amount of time remaning in
        the project work correctly.
        """
        project = Project.factories.base.build(end_date=datetime.date.today() - datetime.timedelta(days=10))
        self.assertEqual(project.days_left, 10)
        self.assertEqual(project.formatted_days_left(), "10 days left")
        project = Project.factories.base.build(end_date=datetime.date.today() - datetime.timedelta(days=1))
        self.assertEqual(project.days_left, 1)
        self.assertEqual(project.formatted_days_left(), "1 day left")
        project = Project.factories.base.build(end_date=datetime.date.today() - datetime.timedelta(minutes=10, days=0))
        self.assertEqual(project.days_left, 0)
        self.assertEqual(project.formatted_days_left(), Project.LESS_THAN_ONE_DAY_LEFT_STATEMENT)
        project = Project.factories.base.build(end_date=datetime.date.today() + datetime.timedelta(days=1))
        self.assertEqual(project.days_left, 0)
        self.assertEqual(project.formatted_days_left(), Project.NO_DAYS_LEFT_STATEMENT)


class ProjectManagerTests(TestCase):
    """Tests for the Project manager"""

    def setUp(self):
        Project.factories.base.create(org_name="The Community Dance Studio", project_status=Project.ACTIVE)
        Project.factories.base.create(org_name="Comoonity Dairy", project_status=Project.COMPLETED)
        Project.factories.base.create(org_name="Educathing", project_status=Project.PROPOSED)
        Project.factories.base.create(org_name="Fire Emblem", project_status=Project.DRAFTED)

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


class CategoryTest(TestCase):
    """Tests that category selection and updating work with projects."""

    def test_update_category(self):
        """ Test that updating a single projects category works """
        project = Project.factories.base.create()
        category1, category2 = Category.factories.base.create_batch(2)
        # tests that associating two categories with the project works
        project.update_categories(Category.valid_categories[:2])
        self.assertEqual(len(project.category_set.all()), 2)
        self.assertItemsEqual(project.category_set.all(), [category1, category2])
        # tests that having no categories with the project works
        project.update_categories([])
        self.assertEqual(len(project.category_set.all()), 0)

    def test_update_category_multiple_projects(self):
        """ Test that removing categories from a project does not affect other projects """
        # creates 2 projects
        project1, project2 = Project.factories.base.create_batch(2)
        # resets the category factory and makes three categories
        Category.factories.base.title.reset()
        category1, category2, category3 = Category.factories.base.create_batch(3)
        # adds categories 1 and 2 to project 1
        project1.update_categories(Category.valid_categories[:2])
        self.assertEqual(len(project1.category_set.all()), 2)
        self.assertItemsEqual(project1.category_set.all(), [category1, category2])
        # adds categories 2 and 3 to project 1
        project2.update_categories(Category.valid_categories[1:3])
        self.assertEqual(len(project2.category_set.all()), 2)
        self.assertItemsEqual(project2.category_set.all(), [category2, category3])
        # removes category 2 from project 1
        project1.update_categories(Category.valid_categories[1:2])
        self.assertEqual(len(project1.category_set.all()), 1)
        self.assertItemsEqual(project1.category_set.all(), [category2])
        # tests that deleting category 2 from project 1 does not affect project 2
        self.assertItemsEqual(project2.category_set.all(), [category2, category3])


class RequestTest(TestCase):
    """Test that all is well with the project pages."""

    def _assert_project_page_works(self, project):
        resp = self.client.get(project.get_absolute_url())
        self.assertNotEqual(resp.status_code, 500)

    def test_project_page(self):
        project = Project.factories.base.create()

        for status_choice in Project.PROJECT_STATUS_CHOICES:
            status = status_choice[0]
            project.project_status = status
            project.save()
            self._assert_project_page_works(project)

    def test_drafted_projects_404(self):
        """Test that the response is 404 when trying to request the page of a drafted project."""
        project = Project.factories.base.create(project_status=Project.DRAFTED)
        resp = self.client.get(project.get_absolute_url())
        self.assertEqual(resp.status_code, 404)


class ProjectIntegrationTest(WebTest):
    def test_only_donate_when_logged_in(self):
        """
        Test that a not logged in user gets redirected to the
        login page instead of being able to donate.
        """
        project = Project.factories.active.create()
        resp = self.app.get("/project/%d/" % project.pk, auto_follow=True)
        self.assertEqual(resp.status_code, 200)
        # note: if the link makes a modal appear, it will be skipped and the
        # test will fail because it couldn't find the link - this is what
        # we want to happen in this case, but we may have to change this if
        # we want a login modal to appear instead.
        resp = (resp.click(linkid="donate-button")).maybe_follow()
        self.assertTemplateUsed(resp, "base/sign_in.html")


class ScrapeTest(TestCase):
    """Test that the scrape task runs with no errors,
        and changes the project's solar data files"""

    def test_scrape(self):
        result = scrape.delay()
        self.assertTrue(result.successful())


class DonationAjaxTestCase(TestUserMixin, TestCase):
    """
    Test suite for AJAX payment donations for projects.
    """
    DONATION = 'donation/submit'

    def setUp(self):
        super(DonationAjaxTestCase, self).setUp()
        self.send_test_user_login_request()
        self.project = Project.factories.base.create(project_status=Project.ACTIVE)

    def perform_valid_donation(self):
        """
        Utility method for performing a valid donation. Returns the response.
        """
        valid_donation = {
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
        return self.client.post(
            self.project.get_absolute_url() + self.DONATION,
            data=valid_donation,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

    def test_valid_donation(self):
        """
        Test valid donation via AJAX to /project/<pk>/donation/submit.
        """
        resp = self.perform_valid_donation()
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIsNone(content.get('error'))
        self.assertIsNotNone(self.project.donors.get(pk=self.test_user.pk))

    @mock.patch('revolv.lib.mailer.EmailMultiAlternatives')
    def test_post_donation_email(self, mock_mailer):
        """
        Tests whether a valid donation will send a revolv email
        """
        resp = self.perform_valid_donation()
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIsNone(content.get('error'))
        self.assertIsNotNone(self.project.donors.get(pk=self.test_user.pk))
        self.assertTrue(mock_mailer.called)
        # checks that the email address sent using mock mailer matches the user who donatred
        args, kwargs = mock_mailer.call_args
        self.assertEqual(kwargs['to'], ["john@example.com"])

    def test_invalid_donation_ajax(self):
        """
        Tests that invalid donation appropriately errors with on
        /donation/submit endpoint.
        """
        invalid_donation = {
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
            self.project.get_absolute_url() + self.DONATION,
            data=invalid_donation,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        content = json.loads(resp.content)
        self.assertEquals(resp.status_code, 400)
        self.assertIsNotNone(content['error'])
