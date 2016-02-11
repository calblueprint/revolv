from django.conf import settings
from django.test import TestCase

from revolv.project.models import Project
from revolv.lib.testing import TestUserMixin


class StripePaymentLoginTest(TestCase):

    def setUp(self):
        self.project = Project.factories.base.create()
        self.stripe_url = '/project/%d/stripe/' % self.project.pk

    def test_stripe_requires_login(self):
        resp = self.client.get(self.stripe_url)
        self.assertRedirects(resp, settings.LOGIN_URL + '?next=' + self.stripe_url)


class StripePaymentTest(TestUserMixin, TestCase):

    def setUp(self):
        super(StripePaymentTest, self).setUp()
        self.project = Project.factories.base.create()
        self.send_test_user_login_request()
        self.stripe_url = '/project/%d/stripe/' % self.project.pk

    def test_stripe_get(self):
        resp = self.client.post(self.stripe_url)
        self.assertEqual(400, resp.status_code)

    def test_stripe_empty_post(self):
        resp = self.client.post(self.stripe_url, {
        })
        self.assertEqual(400, resp.status_code)

    def test_bad_stripe_post(self):
        resp = self.client.post(self.stripe_url, {
            'stripeToken': 'garbage',
            'metadata': 'abc',
            'amount_cents': 1000,
        })
        self.assertEqual(400, resp.status_code)

        # can't have tip be entire amount to be charged
        resp = self.client.post(self.stripe_url, {
            'stripeToken': 'garbage',
            'metadata': 10000,
            'amount_cents': 10000,
        })
        self.assertEqual(400, resp.status_code)

        # can't have tip be more than amount to be charged
        resp = self.client.post(self.stripe_url, {
            'stripeToken': 'garbage',
            'metadata': 10001,
            'amount_cents': 10000,
        })
        self.assertEqual(400, resp.status_code)

    def test_reasonable_stripe_post(self):
        """
        No ability (e.g., Selenium) now to get a real Stripe token from their JS
        library and pass it through; just test a flow that "looks" okay to the
        view.
        """
        resp = self.client.post(self.stripe_url, {
            'stripeToken': 'garbage',
            'metadata': 150,
            'amount_cents': 2000,
        })
        self.assertEqual(200, resp.status_code)
        self.assertTemplateUsed(resp, "project/project_donate_error.html")
