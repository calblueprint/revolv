from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from revolv.base.models import RevolvUserProfile
from revolv.lib.testing import TestUserMixin, UserTestingMixin
from revolv.project.models import Category


class CategorySetterTestCase(TestUserMixin, UserTestingMixin, TestCase):
    
    def test_http_redirect(self):
        """
        This test checks to make sure that the CategoryPreferenceSetterView in revolv.base.views 
        redirects to the dashboard when called with an HTTP method that is not allowed (any method except
        POST).

        This test sends a get request to the CategoryPreferenceSetterView, follows the chain of redirects,
        and ensures that the template used in the final view is base/dashboard.html.
        """
        self.test_profile.make_administrator()
        response = self.send_test_user_login_request()
        response = self.client.get(reverse('dashboard_category_setter'), HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
        self.assertTemplateUsed(response, "base/dashboard.html")


    def test_category_setting(self):
        """
        This test checks to make sure that the CategoryPreferenceSetterView in revolv.base.views works.
        What the view should do is take in a dictionary of category ids matched to empty strings,
        clear the user's preferred categories, and then add every category corresponding to the ids
        in the dictionary to the user's preferred categories.

        This test creates a user and then verifies that the user has 0 categories in their preferred categories.
        It then passes a dictionary with 2 category ids to the CategoryPreferenceSetterView, and then checks that
        both of those categories and no other categories are in the user's preferred categories.

        It then passes in a dictionary with 1 category id to the CategoryPreferenceSetterView, and then checks that
        the original 2 ids were removed from the preferred categories, and the newly passed in one was added.
        """
        self.test_profile.make_administrator()
        response = self.send_test_user_login_request()

        # checks to see that the user has no pre-existing preferences
        self.assertEqual(len(self.test_profile.preferred_categories.all()), 0)

        all_category_objects = Category.objects.all()
        id_one = all_category_objects[0].id
        id_two = all_category_objects[1].id
        id_three = all_category_objects[2].id
        
        self.client.post(reverse('dashboard_category_setter'), {id_one: '', id_two: ''}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # checks to see that categories 1 and 2 have been added
        self.assertEqual(len(self.test_profile.preferred_categories.all()), 2)
        self.assertTrue(self.test_profile.preferred_categories.all().filter(id=id_one).exists())
        self.assertTrue(self.test_profile.preferred_categories.all().filter(id=id_two).exists())

        self.client.post(reverse('dashboard_category_setter'), {id_three: ''}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # checks to see that categories 1 and 2 have been removed and category 3 has been added
        self.assertEqual(len(self.test_profile.preferred_categories.all()), 1)
        self.assertTrue(self.test_profile.preferred_categories.all().filter(id=id_three).exists())
        self.assertFalse(self.test_profile.preferred_categories.all().filter(id=id_one).exists())
        self.assertFalse(self.test_profile.preferred_categories.all().filter(id=id_two).exists())

class AuthPagesTestCase(UserTestingMixin, TestUserMixin, TestCase):
    SIGNIN_URL = "/signin/"
    LOGIN_URL = "/login/"
    LOGOUT_URL = "/logout/"
    SIGNUP_URL = "/signup/"
    HOME_URL = "/"

    def test_page_found(self):
        """Test that we can actually render a page."""
        response = self.client.get("/signin/")
        self.assertEqual(response.status_code, 200)

    def test_login_endpoint(self):
        """Test that the login endpoint correctly logs in a user."""
        response = self.send_test_user_login_request()
        self.assertEqual(response.context["user"], self.test_user)
        self.assertUserAuthed(response)

    def test_garbage_login(self):
        response = self.client.post(self.LOGIN_URL, {
            "username": "hjksadhfiobhv",
            "password": "njnpvbebijrwehgjsd"
        }, follow=True)
        self.assertTemplateUsed(response, "base/sign_in.html")
        self.assertNoUserAuthed(response)

    def test_login_logout(self):
        """
        Test that after logging in, the user object can be correctly
        logged out.
        """
        self.send_test_user_login_request()
        response = self.client.get(self.SIGNIN_URL, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        response = self.client.get(self.LOGIN_URL, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        response = self.client.get(self.LOGOUT_URL, follow=True)
        self.assertNoUserAuthed(response)

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

        response = self.client.post(self.SIGNUP_URL, no_name_data, follow=True)  # maybe SIGNIN_URL instead?
        self.assertTemplateUsed(response, "base/sign_in.html")
        self.assertNoUserAuthed(response)

        response = self.client.post(self.SIGNUP_URL, no_email_data, follow=True)
        self.assertTemplateUsed(response, "base/sign_in.html")
        self.assertNoUserAuthed(response)

        response = self.client.post(self.SIGNUP_URL, valid_data, follow=True)
        self.assertRedirects(response, self.HOME_URL)
        self.assertUserAuthed(response)

        # make sure the user was actually saved
        test_user = User.objects.get(username="john123")
        RevolvUserProfile.objects.get(user=test_user)
