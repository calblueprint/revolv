from django.core import mail
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.lib.mailer import send_revolv_email


class MailerTestCase(TestCase):
    email_template_name = "test"
    email_template_context = {
        "names": ["noah", "vivekbloop", "jaylin", "anthonyy", "ericbloop"]
    }

    def test_send_email(self):
        """Test that we can send email correctly."""
        send_revolv_email(
            self.email_template_name,
            self.email_template_context,
            ["me@example.com"]
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "What's the best team in Blueprint?"
        )
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], "me@example.com")

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
