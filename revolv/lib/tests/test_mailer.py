import datetime

import mock
from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email
from revolv.payments.models import Payment, PaymentType
from revolv.project.models import Project


class MailerTestCase(TestCase):
    email_template_name = "test"
    email_template_context = {
        "names": ["noah", "vivekbloop", "jaylin", "anthonyy", "ericbloop"]
    }

    def test_send_email(self):
        """Test that we can send email correctly."""
        success = send_revolv_email(
            self.email_template_name,
            self.email_template_context,
            ["me@example.com"]
        )
        self.assertEqual(success, 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "What's the best team in Blueprint?"
        )
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], "me@example.com")

    def test_fails_silently(self):
        """Test that invalid email parameters raise an error if we tell them to."""
        send_revolv_email(
            self.email_template_name,
            self.email_template_context,
            ["mejksldafs"],
            from_email="INVALID##&^%%%^*!  #Y* #$H*",
            fail_silently=True
        )
        with mock.patch("revolv.lib.mailer.EmailMultiAlternatives.send", side_effect=Exception):
            with self.assertRaises(Exception):
                send_revolv_email(
                    self.email_template_name,
                    self.email_template_context,
                    ["mejksldafs"],
                    from_email="INVALID##&^%%%^*!  #Y* #$H*",
                    fail_silently=False
                )

    def test_cc_admins(self):
        """
        Test that all admin users will be cc'd if the cc_admins flag is
        passed to send_revolv_email.
        """
        RevolvUserProfile.objects.create_user_as_admin("a", "a@a.com", "apass")
        RevolvUserProfile.objects.create_user_as_admin("b", "b@b.com", "bpass")
        send_revolv_email(
            self.email_template_name,
            self.email_template_context,
            ["me@example.com"],
            cc_admins=True
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("a@a.com", mail.outbox[0].cc)
        self.assertIn("b@b.com", mail.outbox[0].cc)


class MonthlyDonationEmailTestCase(TestCase):
    def test_monthly_donation_email_no_donations(self):
        """
        Tests that if there are no donations, nothing will be sent
        """
        RevolvUserProfile.factories.base.create()
        call_command('monthlydonationemail', override=True)
        self.assertEqual(len(mail.outbox), 0)

    def test_monthly_donation_email(self):
        """
        Tests that with two donations in the past month from two different users,
        the Revolv Mailer send two emails
        """
        # creates 2 users and 2 projects
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        project1, project2 = Project.factories.base.create_batch(2)

        # gets a day from the last month
        date_of_last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)

        # creates two payments and sets their created_at date to a date from last month
        Payment.factories.base.create(
            user=user1,
            entrant=user1,
            payment_type=PaymentType.objects.get_paypal(),
            project=project1,
            created_at=date_of_last_month
        )

        Payment.factories.base.create(
            user=user2,
            entrant=user2,
            payment_type=PaymentType.objects.get_paypal(),
            project=project2,
            created_at=date_of_last_month
        )

        call_command('monthlydonationemail', override=True)
        self.assertEqual(len(mail.outbox), 2)

    def test_monthly_donation_email_no_donations_in_past_month(self):
        """
        Tests that with two donations from a year ago from two different users,
        the Revolv Mailer send no emails
        """
        # creates 2 users and 2 projects
        user1, user2 = RevolvUserProfile.factories.base.create_batch(2)
        project1, project2 = Project.factories.base.create_batch(2)

        # gets a day from last year
        date_from_last_year = datetime.date.today() - datetime.timedelta(days=365)

        # creates two payments and sets their created_at date to a date from last year
        Payment.factories.base.create(
            user=user1,
            entrant=user1,
            payment_type=PaymentType.objects.get_paypal(),
            project=project1,
            created_at=date_from_last_year
        )

        Payment.factories.base.create(
            user=user2,
            entrant=user2,
            payment_type=PaymentType.objects.get_paypal(),
            project=project2,
            created_at=date_from_last_year
        )

        call_command('monthlydonationemail', override=True)
        self.assertEqual(len(mail.outbox), 0)
