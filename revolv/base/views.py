from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Website home page. THIS VIEW IS INCOMPLETE. UPDATE DOCSTRING
    WHEN COMPLETED."""
    template_name = 'base/home.html'


class SignInView(TemplateView):
    """Signup and login page. Has three submittable forms: login, signup,
    and sign in with facebook.

    Note that the signup with facebook functionality will automatically
    create a user object, but if the user has previously signed up with
    facebook, they will not be able to sign in without facebook to the
    same account.

    Also note that the "sign in with facebook" does not necessarily do
    the same thing as either sign up or login: when the user clicks this
    button, they will be automatically signed up and logged in if there
    is not an account associated with their facebook profile, or they will
    just be logged in if there is.
    """
    template_name = "base/sign_in.html"
