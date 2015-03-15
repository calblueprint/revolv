from django.test import TestCase
from revolv.lib.testing import TestUserMixin


class UserDataMixinTestCase(TestUserMixin, TestCase):
    def test_donor(self):
        response = self.send_test_user_login_request()
        self.assertEqual(response.context["is_donor"], True)
        self.assertEqual(response.context["is_ambassador"], False)
        self.assertEqual(response.context["is_administrator"], False)

    def test_ambassador(self):
        self.test_profile.make_ambassador()
        response = self.send_test_user_login_request()
        self.assertEqual(response.context["is_donor"], True)
        self.assertEqual(response.context["is_ambassador"], True)
        self.assertEqual(response.context["is_administrator"], False)

    def test_admin(self):
        self.test_profile.make_administrator()
        response = self.send_test_user_login_request()
        self.assertEqual(response.context["is_donor"], True)
        self.assertEqual(response.context["is_ambassador"], True)
        self.assertEqual(response.context["is_administrator"], True)
