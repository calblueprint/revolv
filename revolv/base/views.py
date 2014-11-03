from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView
from revolv.base.forms import SignupForm
from revolv.base.models import RevolvUserProfile
from revolv.project.models import Project


class HomePageView(TemplateView):
    """Website home page. THIS VIEW IS INCOMPLETE. UPDATE DOCSTRING
    WHEN COMPLETED."""
    template_name = 'base/home.html'
    NUM_PROJECTS_SHOWN = 1000

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.get_featured(
            HomePageView.NUM_PROJECTS_SHOWN)
        return context


class UserDataMixin(object):
    def deny_access(self):
        """Basic method to replace the default PermissionDenied()"""
        messages.error(
            self.request,
            'Oops! You do not have permission to access this page.'
        )
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        """ dispatch() gets request.user and downcasts self.user to the actual
        user type, if possible. If the user isn't logged in, then self.user is
        an AnonymousUser, which is a built-in Django user type. If the user is
        logged in, self.user is a django.contrib.auth.models.User.
        """
        self.user = request.user
        if self.user.is_authenticated():
            self.user_profile = RevolvUserProfile.objects.get(user=self.user)
            self.is_donor = self.user_profile.is_donor()
            self.is_ambassador = self.user_profile.is_ambassador()
            self.is_administrator = self.user_profile.is_administrator()
        else:
            self.is_donor = False
            self.is_ambassador = False
            self.is_administrator = False
        return super(UserDataMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """ 'revolv_user' is included here for convenience. By default, the
        variable {{ user }} in the templates refers to 'request.user' above,
        which is either an AnonymousUser or a User with a RevolvUserProfile.
        We may want access to attributes in the downcasted user type, so to
        access these we can use {{ revolv_user }} in the templates.
        """
        context = super(UserDataMixin, self).get_context_data(**kwargs)
        context['revolv_user'] = self.user
        context['is_donor'] = self.is_donor
        context['is_ambassador'] = self.is_ambassador
        context['is_administrator'] = self.is_administrator
        return context


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

    Http verbs:
        GET: renders the signin page with empty forms.
    """
    template_name = "base/sign_in.html"
    login_form_class = AuthenticationForm
    signup_form_class = SignupForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("home")
        return super(SignInView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(SignInView, self).get_context_data(**kwargs)
        login_form = self.login_form_class()
        signup_form = self.signup_form_class()
        context["signup_form"] = signup_form
        context["login_form"] = login_form
        return context


class RedirectToSigninOrHomeMixin(object):
    """
    Mixin that detects if a page was requested with method="GET", and redirects
    to the signin page if so. Also, if posted to with an already authenticated
    user, will redirect to the homepage instead.

    This is useful both for the login and signup endpoints.
    """
    @method_decorator(sensitive_post_parameters(
        "password", "password1", "password2"
    ))
    def dispatch(self, request, *args, **kwargs):
        # don't allow rendering a form page with a GET request to this view:
        # instead, redirect to the signin page
        if self.request.method == "GET":
            return redirect("signin")
        # if the user is already logged in and tries to log in again, just
        # redirect them to the home page.
        if request.user.is_authenticated():
            return redirect("home")
        return super(RedirectToSigninOrHomeMixin, self).dispatch(
            request, *args, **kwargs
        )


class LoginView(RedirectToSigninOrHomeMixin, FormView):
    """
    Login endpoint: checks the data from the received request against
    django.contrib.auth.forms.AuthenticationForm and logs in the user if
    possible. If not, redirects back to the signin page.

    Http verbs:
        GET: redirect to signin page
        POST: check post parameters for user credentials, login the user
            and redirect to the specified next page (home by default), or
            redirect back to signin page.

    Todo(noah): add in form error messages for the signin page.
    """
    form_class = AuthenticationForm

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        self.next_url = request.POST.get("next", "home")
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        return redirect("signin")

    def form_valid(self, form):
        """Log the user in and redirect them to the supplied next page."""
        auth_login(self.request, form.get_user())
        return redirect(self.next_url)


class SignupView(RedirectToSigninOrHomeMixin, FormView):
    """
    Signup endpoint: processes the signup form and signs the user up (and logs
    them in). Note that the sign up with facebook functionality is entirely
    different: this is only for the regular django auth signup flow.

    Http verbs:
        GET: redirect to signin page
        POST: check post params against form, redirect to signin page if the
            form is not valid.

    Todo(noah): add in form error messages for the signin page
    """
    form_class = SignupForm

    def form_invalid(self, form):
        return redirect("signin")

    def form_valid(self, form):
        form.save()
        # log in the newly created user model. if there is a problem, error
        auth_login(self.request, form.ensure_authenticated_user())
        return redirect("home")
