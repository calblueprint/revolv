from django.contrib.auth.models import User
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.base.utils import get_group_by_name
from revolv.lib.testing import TestUserMixin, UserTestingMixin


class RevolvUserProfileManagerTestCase(TestCase):
    """Tests for the RevolvUserProfileManager."""

    def test_get_subscribed_to_newsletter(self):
        """Test that we can correctly query users that are subscribed to the newsletter."""
        RevolvUserProfile.factories.base.create_batch(2, subscribed_to_newsletter=False)
        RevolvUserProfile.factories.base.create_batch(2, subscribed_to_newsletter=True, user__email="revolv@gmail.com")
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


class ProfileTestCase(TestUserMixin, UserTestingMixin, TestCase):
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
