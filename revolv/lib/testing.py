from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.forms.models import model_to_dict, modelform_factory
from revolv.base.utils import get_profile
from revolv.lib.webtest.form_fillers import FILLERS


class TestUserMixin(object):
    """
    A testing mixin which ensures that there is a self.test_user for every test.
    Note that this is different from UserTestingMixin, which provides utility methods
    for testing things about users. They are seperated because there's no need to
    do extra database operations if you don't need to access self.test_user ever.
    """

    def send_user_login_request(self, user, password, webtest=False):
        """Send a request to login the user then return the response."""
        if webtest:
            client = self.app
            kwargs = {}
        else:
            client = self.client
            kwargs = {"follow": True}

        response = client.post(
            "/login/",
            {
                "username": user.get_username(),
                "password": password
            },
            **kwargs
        )
        if webtest:
            response = response.maybe_follow()
        return response

    def send_test_user_login_request(self, webtest=False):
        """Send a request to login the test user then return the response."""
        return self.send_user_login_request(self.test_user, "test_user_password", webtest)

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


class WebTestMixin(object):
    """
    A testing mixin which provides additional functionality for integration tests
    using WebTest.
    """

    def fill_form_from_model(self, webtest_form, model_instance, model_name=None, warn_of_errors=False):
        """"
        Given a WebTest form which was rendered from a django ModelForm,
        fill out as much of it as possible from the model, then return the filled
        out form.

        This method will look at the fields of the form, and for every field, it will
        check for a corresponding field on the model. If that exists, it will try to set the
        field of the form to be the corresponding value from the model instance. It
        makes no guarentee about whether the fields can be set, and will error if they
        cannot.

        If model_name is provided, it should be the name of a model, like "Project". This function
        will check to see if there is a webtest FormFiller defined in revolv/lib/webtest/form_fillers.py,
        and if so will use it to further fill the form. This strategy can be useful when we want to
        have things like project cover_photo which are required by the form but default to none -
        the form filler will take care of populating the form with a dummy cover_photo.

        If warn_of_errors is true, this method will print out all the errors of the ModelForm
        which it is supposed to be filling out. Can be useful to triage which fields of the form
        are ignored by the default filling algorithm and thus must be used by a webtest FormFiller.
        """
        ThisModelForm = modelform_factory(type(model_instance))
        model_form_instance = ThisModelForm(instance=model_instance, data=model_to_dict(model_instance))
        model_form_instance.is_valid()  # trigger data clean to make cleaned_data available
        for field_name, field_value in webtest_form.fields.items():
            if field_name is None:  # for the submit button, the field name is none
                continue
            field_model_value = model_form_instance.cleaned_data.get(field_name)
            if field_model_value:
                webtest_form[field_name] = str(field_model_value)
            else:
                print "[WebTestMixin.fill_form_from_model] WARNING: no field for " + str(field_name)

        if model_name is not None and FILLERS.get(model_name) is not None:
            webtest_form = FILLERS[model_name](webtest_form, model_instance).fill_form()

        return webtest_form

    def assert_id_in_response_html(self, response, id):
        """
        Given the html of a WebTest response (response.html), assert that the given id
        exists in that response's DOM.
        """
        query = BeautifulSoup(response.html)
        # we want to make sure that there is a password reset link (not just a url) in the email
        element = query.find(id=id)
        self.assertIsNotNone(element)
