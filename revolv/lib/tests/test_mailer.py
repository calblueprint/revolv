import datetime
import os

import mock
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email
from revolv.payments.models import Payment


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
        Tests that if there are no donations, nothing will be sent to any users, but
        an email notification will be sent to administrators.

        Also tests the silence_admin_notifications flag.
        """
        # creates a regular user
        RevolvUserProfile.factories.base.create()
        # creates an administrator user
        RevolvUserProfile.factories.admin.create()

        with open(os.devnull, 'w') as f:
            call_command('monthlydonationemail', override=True, stdout=f, silence_admin_notifications=True)
            self.assertEqual(len(mail.outbox), 0)
            call_command('monthlydonationemail', override=True, stdout=f)
            self.assertEqual(len(mail.outbox), 1)

    def test_monthly_donation_email(self):
        """
        Tests that with two donations in the past month from two different users,
        the Revolv Mailer send two emails
        """
        # gets a day from the last month
        date_of_last_month = timezone.now().replace(day=1) - datetime.timedelta(days=1)

        # creates two payments and sets their created_at date to a date from last month
        Payment.factories.base.create(
            created_at=date_of_last_month
        )

        Payment.factories.base.create(
            created_at=date_of_last_month
        )

        with open(os.devnull, 'w') as f:
            call_command('monthlydonationemail', override=True, stdout=f)
            self.assertEqual(len(mail.outbox), 2)

    def test_monthly_donation_email_no_donations_in_past_month(self):
        """
        Tests that with two donations from a year ago from two different users,
        the Revolv Mailer send no emails
        """
        # gets a day from last year
        date_from_last_year = timezone.now() - datetime.timedelta(days=365)

        # creates two payments and sets their created_at date to a date from last year
        Payment.factories.base.create(
            created_at=date_from_last_year
        )

        Payment.factories.base.create(
            created_at=date_from_last_year
        )

        with open(os.devnull, 'w') as f:
            call_command('monthlydonationemail', override=True, stdout=f)
            self.assertEqual(len(mail.outbox), 0)

    def test_monthly_donation_email_not_first_day_of_month_override(self):
        """
        Tests that if monthlydonationemail is called on a day which is not the first of the month,
        it'll only email for payments from the last month, not from the last thirty days.

        Calling on 3/5 won't email for payments on 3/2, but will for payments on 2/2.
        """
        # gets a day from the last month
        february_payment = datetime.datetime(2013, 2, 2)
        march_payment = datetime.datetime(2013, 3, 3)
        with mock.patch.object(timezone, 'now', return_value=datetime.datetime(2013, 3, 4)):
            Payment.factories.base.create(
                created_at=february_payment
            )
            Payment.factories.base.create(
                created_at=march_payment
            )
            with open(os.devnull, 'w') as f:
                call_command('monthlydonationemail', override=True, stdout=f)
                self.assertEqual(len(mail.outbox), 1)

    def test_monthly_donation_email_first_day_of_month(self):
        """
        Tests that the monthlydonationemail command actually runs on the first day of the month with no override.
        """
        payment_created_at = datetime.datetime(2013, 1, 30)
        with mock.patch.object(timezone, 'now', return_value=datetime.datetime(2013, 2, 1)):

            Payment.factories.base.create(
                created_at=payment_created_at
            )

            with open(os.devnull, 'w') as f:
                call_command('monthlydonationemail', stdout=f)
                self.assertEqual(len(mail.outbox), 1)
