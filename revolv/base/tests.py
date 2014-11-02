from django.contrib.auth.models import User
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.base.utils import get_group_by_name


class SmokeTestCase(TestCase):
    def test_works(self):
        """Test that the test framework works."""
        self.assertEqual(1, 1)


class UserAuthTestCase(TestCase):
    SIGNIN_URL = "/signin/"
    LOGIN_URL = "/login/"
    LOGOUT_URL = "/logout/"
    SIGNUP_URL = "/signup/"
    HOME_URL = "/"

    def _send_test_user_login_request(self):
        response = self.client.post(
            "/login/",
            {
                "username": self.test_user.get_username(),
                "password": "test_user_password"
            },
            follow=True
        )
        return response

    def _assert_no_user_authed(self, response):
        self.assertFalse(response.context["user"].is_authenticated())

    def _assert_user_authed(self, response):
        self.assertTrue(response.context["user"].is_authenticated())

    def setUp(self):
        """Every test in this case has a test user."""
        self.test_user = User.objects.create_user(
            "John",
            "john@example.com",
            "test_user_password"
        )

    def test_user_profile_sync(self):
        """
        Test that saving/deleting a User will get/create/delete the
        appropriate user profile as well.

        Note: django 1.7 removes support for user.get_profile(), so we test
        here that we can access a user's profile using user.revolvuserprofile.
        """
        profile = RevolvUserProfile.objects.filter(user=self.test_user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile, self.test_user.revolvuserprofile)

        self.test_user.last_name = "Doe"
        self.test_user.save()

        profiles = RevolvUserProfile.objects.filter(user=self.test_user)
        self.assertEqual(len(profiles), 1)

        self.test_user.delete()
        profile = RevolvUserProfile.objects.filter(user=self.test_user).first()
        self.assertIsNone(profile)

    def test_login_endpoint(self):
        """Test that the login endpoint correctly logs in a user."""
        response = self._send_test_user_login_request()
        self.assertEqual(response.context["user"], self.test_user)
        self.assertTrue(response.context["user"].is_authenticated())

    def test_garbage_login(self):
        response = self.client.post(self.LOGIN_URL, {
            "username": "hjksadhfiobhv",
            "password": "njnpvbebijrwehgjsd"
        }, follow=True)
        self.assertRedirects(response, self.SIGNIN_URL)
        self._assert_no_user_authed(response)

    def test_login_logout(self):
        """
        Test that after logging in, the user object can be correctly
        logged out.
        """
        self._send_test_user_login_request()
        response = self.client.get(self.SIGNIN_URL, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        response = self.client.get(self.LOGIN_URL, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        response = self.client.get(self.LOGOUT_URL, follow=True)
        self._assert_no_user_authed(response)

    def test_signup_endpoint(self):
        """Test that we can create a new user through the signup form."""
        valid_data = {
            "username": "john123",
            "password1": "doe_password_1",
            "password2": "doe_password_1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        }

        no_name_data = valid_data.copy()
        no_name_data["first_name"] = ""

        no_email_data = valid_data.copy()
        no_email_data["email"] = ""

        response = self.client.post(self.SIGNUP_URL, no_name_data, follow=True)
        self.assertRedirects(response, self.SIGNIN_URL)
        self._assert_no_user_authed(response)

        response = self.client.post(
            self.SIGNUP_URL,
            no_email_data,
            follow=True
        )
        self.assertRedirects(response, self.SIGNIN_URL)
        self._assert_no_user_authed(response)

        response = self.client.post(self.SIGNUP_URL, valid_data, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        self._assert_user_authed(response)
        # make sure the user was actually saved
        User.objects.get(username="john123")


class UserPermissionsTestCase(TestCase):
    fixtures = ['base_groups.json', 'base_permissions.json']

    def setUp(self):
        """Every test in this case has a test user."""
        self.test_user = User.objects.create_user(
            "permissionTestUser",
            "john@example.com",
            "permission_test_user_password"
        )

    def _assert_group_relationship(self, user, group_name, relIn):
        group = get_group_by_name(group_name)
        if relIn:
            self.assertIn(group, user.groups.all())
        else:
            self.assertNotIn(group, user.groups.all())

    def _assert_in_group(self, user, group_name):
        return self._assert_group_relationship(user, group_name, True)

    def _assert_not_in_group(self, user, group_name):
        return self._assert_group_relationship(user, group_name, False)

    def _assert_groups_correct(self, user, ambassador, admin,
                               ambassador_perm=None, admin_perm=None):
        if ambassador:
            amb_group_check = self._assert_in_group
        else:
            amb_group_check = self._assert_not_in_group

        if admin:
            ad_group_check = self._assert_in_group
        else:
            ad_group_check = self._assert_not_in_group

        amb_group_check(user, RevolvUserProfile.AMBASSADOR_GROUP)
        ad_group_check(user, RevolvUserProfile.ADMIN_GROUP)

    def test_correct_groups_exist(self):
        get_group_by_name(RevolvUserProfile.AMBASSADOR_GROUP)
        get_group_by_name(RevolvUserProfile.ADMIN_GROUP)

    def test_all_users_are_donors(self):
        self.assertTrue(self.test_user.revolvuserprofile.is_donor())
        self._assert_groups_correct(self.test_user, False, False)

    def test_ambassadors(self):
        self.test_user.revolvuserprofile.make_ambassador()
        self._assert_groups_correct(
            self.test_user, ambassador=True, admin=False
        )

        self.test_user.revolvuserprofile.make_donor()
        self._assert_groups_correct(
            self.test_user, ambassador=False, admin=False
        )

    def test_admins(self):
        self.test_user.revolvuserprofile.make_admin()
        self._assert_groups_correct(
            self.test_user,
            ambassador=False,
            admin=True,
            ambassador_perm=True,
            admin_perm=True
        )

        self.test_user.revolvuserprofile.make_ambassador()
        self._assert_groups_correct(
            self.test_user, ambassador=True, admin=False
        )
        self.test_user.revolvuserprofile.make_donor()
        self._assert_groups_correct(
            self.test_user, ambassador=False, admin=False
        )


class LoginSignupPageTestCase(TestCase):
    def test_page_found(self):
        """Test that we can actually render a page."""
        response = self.client.get("/signin/")
        self.assertEqual(response.status_code, 200)
