from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.models.signals import post_save
from django.test import TestCase
from django_facebook.utils import get_user_model
from revolv.base.models import RevolvUserProfile
from revolv.base.signals import create_profile_of_user
from revolv.base.utils import get_group_by_name, get_profile


class TestUserMixin(object):
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

    def _bust_test_user_cache(self):
        self.test_user = User.objects.get(username=self.test_user.username)
        self.test_profile = get_profile(self.test_user)

    def setUp(self):
        """Every test in this case has a test user."""
        self.test_user = User.objects.create_user(
            "John",
            "john@example.com",
            "test_user_password"
        )
        self.test_profile = get_profile(self.test_user)


class UserAuthTestCase(TestUserMixin, TestCase):
    SIGNIN_URL = "/signin/"
    LOGIN_URL = "/login/"
    LOGOUT_URL = "/logout/"
    SIGNUP_URL = "/signup/"
    HOME_URL = "/"

    def _assert_no_user_authed(self, response):
        self.assertFalse(response.context["user"].is_authenticated())

    def _assert_user_authed(self, response):
        self.assertTrue(response.context["user"].is_authenticated())

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
        self.assertTemplateUsed(response, "base/sign_in.html")
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
            "email": "john@example.com",
            "subscribed_to_newsletter": True
        }

        no_name_data = valid_data.copy()
        no_name_data["first_name"] = ""

        no_email_data = valid_data.copy()
        no_email_data["email"] = ""

        response = self.client.post(self.SIGNUP_URL, no_name_data, follow=True)
        self.assertTemplateUsed(response, "base/sign_in.html")
        self._assert_no_user_authed(response)

        response = self.client.post(
            self.SIGNUP_URL,
            no_email_data,
            follow=True
        )
        self.assertTemplateUsed(response, "base/sign_in.html")
        self._assert_no_user_authed(response)

        response = self.client.post(self.SIGNUP_URL, valid_data, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        self._assert_user_authed(response)
        # make sure the user was actually saved
        test_user = User.objects.get(username="john123")
        RevolvUserProfile.objects.get(user=test_user)


class RevolvUserProfileManagerTestCase(TestCase):
    """Tests for the RevolvUserProfileManager
        TODO : Update test to create test objects and not load fixtures.
    """

    def setUp(self):
        post_save.disconnect(receiver=create_profile_of_user, sender=get_user_model())
        call_command('loaddata', 'user', 'revolvuserprofile', 'project')

    def tearDown(self):
        post_save.connect(create_profile_of_user, sender=get_user_model())

    def test_get_subscribed_to_newsletter(self):
        context = RevolvUserProfile.objects.get_subscribed_to_newsletter()
        self.assertEqual(len(context), 2)
        self.assertEqual(context[0], "revolv@gmail.com")


class UserPermissionsTestCase(TestCase):

    def setUp(self):
        """Every test in this case has a test user."""
        self.test_user = User.objects.create_user(
            "permissionTestUser",
            "john@example.com",
            "permission_test_user_password"
        )

    def _assert_group_relationship(self, user, group_name, rel_in):
        """Assert that a user is or is not in a given group.

        :user: {User} the user to check
        :group_name: {string} the group name to check
        :rel_in: {boolean} if true, assert that the user is IN the group.
                 otherwise, assert that the user is NOT in the group
        """
        group = get_group_by_name(group_name)
        if rel_in:
            self.assertIn(group, user.groups.all())
        else:
            self.assertNotIn(group, user.groups.all())

    def _assert_in_group(self, user, group_name):
        """Assert that the given User is in the group specified by group_name."""
        return self._assert_group_relationship(user, group_name, True)

    def _assert_not_in_group(self, user, group_name):
        """Assert that the given User is not in the group specified by group_name."""
        return self._assert_group_relationship(user, group_name, False)

    def _assert_groups_correct(self, user, ambassador, admin):
        """
        Given a User: if ambassador is True, assert that the user is an
        ambassador. Additionally, if admin is True, also assert that the
        user is an administrator.
        """
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
        self.assertFalse(self.test_user.is_staff)

        self.test_user.revolvuserprofile.make_donor()
        self._assert_groups_correct(
            self.test_user, ambassador=False, admin=False
        )
        self.assertFalse(self.test_user.is_staff)

    def test_admins(self):
        self.test_user.revolvuserprofile.make_administrator()
        self._assert_groups_correct(
            self.test_user,
            ambassador=True,
            admin=True
        )
        self.assertTrue(self.test_user.is_staff)

        self.test_user.revolvuserprofile.make_ambassador()
        self._assert_groups_correct(
            self.test_user, ambassador=True, admin=False
        )
        self.assertFalse(self.test_user.is_staff)

        self.test_user.revolvuserprofile.make_donor()
        self._assert_groups_correct(
            self.test_user, ambassador=False, admin=False
        )
        self.assertFalse(self.test_user.is_staff)

        self.test_user.revolvuserprofile.make_administrator()
        self._assert_groups_correct(
            self.test_user,
            ambassador=True,
            admin=True
        )
        self.assertTrue(self.test_user.is_staff)


class UserDataMixinTestCase(TestUserMixin, TestCase):
    def test_donor(self):
        response = self._send_test_user_login_request()
        self.assertEqual(response.context["is_donor"], True)
        self.assertEqual(response.context["is_ambassador"], False)
        self.assertEqual(response.context["is_administrator"], False)

    def test_ambassador(self):
        get_profile(self.test_user).make_ambassador()
        response = self._send_test_user_login_request()
        self.assertEqual(response.context["is_donor"], True)
        self.assertEqual(response.context["is_ambassador"], True)
        self.assertEqual(response.context["is_administrator"], False)

    def test_admin(self):
        get_profile(self.test_user).make_administrator()
        response = self._send_test_user_login_request()
        self.assertEqual(response.context["is_donor"], True)
        self.assertEqual(response.context["is_ambassador"], True)
        self.assertEqual(response.context["is_administrator"], True)


class LoginSignupPageTestCase(TestCase):
    def test_page_found(self):
        """Test that we can actually render a page."""
        response = self.client.get("/signin/")
        self.assertEqual(response.status_code, 200)


class DashboardTestCase(TestUserMixin, TestCase):
    DASH_BASE = "/dashboard/"
    ADMIN_DASH = "/dashboard/admin/"
    AMBAS_DASH = "/dashboard/ambassador/"
    DONOR_DASH = "/dashboard/donor/"
    HOME_URL = "/"

    def test_dash_redirects(self):
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.HOME_URL)

        self._send_test_user_login_request()
        self.test_user.revolvuserprofile.make_administrator()
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.ADMIN_DASH)

        self.test_user.revolvuserprofile.make_ambassador()
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.AMBAS_DASH)

        self.test_user.revolvuserprofile.make_donor()
        response = self.client.get(self.DASH_BASE, follow=True)
        self.assertRedirects(response, self.DONOR_DASH)
