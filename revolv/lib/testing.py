from django.contrib.auth.models import User
from revolv.base.utils import get_profile


class TestUserMixin(object):
    """
    A testing mixin which ensures that there is a self.test_user for every test.
    Note that this is different from UserTestingMixin, which provides utility methods
    for testing things about users. They are seperated because there's no need to
    do extra database operations if you don't need to access self.test_user ever.
    """

    def send_test_user_login_request(self):
        """Send a request to login the test user then return the response."""
        response = self.client.post(
            "/login/",
            {
                "username": self.test_user.get_username(),
                "password": "test_user_password"
            },
            follow=True
        )
        return response

    def bust_test_user_cache(self):
        """Make sure that the user and profile are up to date (avoid db caching)."""
        self.test_user = User.objects.get(username=self.test_user.username)
        self.test_profile = get_profile(self.test_user)

    def setUp(self):
        """Every test in this mixin has a test user."""
        self.test_user = User.objects.create_user(
            "John",
            "john@example.com",
            "test_user_password"
        )
        self.test_profile = get_profile(self.test_user)


class UserTestingMixin(object):
    """
    A testing mixin which provides various utility methods for testing things
    related to user accounts and profiles.
    """

    def assertNoUserAuthed(self, response):
        """Given a response, assert that there IS NOT a user authenticated in the session."""
        self.assertFalse(response.context["user"].is_authenticated())

    def assertUserAuthed(self, response):
        """Given a response, assert that there IS a user authenticated in the session."""
        self.assertTrue(response.context["user"].is_authenticated())
