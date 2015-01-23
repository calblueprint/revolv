from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView, View
from revolv.base.forms import SignupForm
from revolv.base.users import UserDataMixin
from revolv.payments.models import Payment
from revolv.project.models import Project


class HomePageView(UserDataMixin, TemplateView):
    """Website home page. THIS VIEW IS INCOMPLETE. UPDATE DOCSTRING
    WHEN COMPLETED."""
    template_name = 'base/home.html'
    NUM_PROJECTS_SHOWN = 1000

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["featured_projects"] = Project.objects.get_featured(
            HomePageView.NUM_PROJECTS_SHOWN)
        context["completed_projects_count"] = Project.objects.get_completed().count()
        context["total_donors_count"] = Payment.objects.total_distinct_donors()
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
        context["login_redirect_url"] = self.request.GET.get("next")
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
            render the sign in page with errors.
    """
    form_class = AuthenticationForm
    template_name = 'base/sign_in.html'

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        self.next_url = request.POST.get("next", "home")
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Log the user in and redirect them to the supplied next page."""
        auth_login(self.request, form.get_user())
        messages.success(self.request, 'Logged in as ' + self.request.POST.get('username'))
        return redirect(self.next_url)

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(*args, **kwargs)
        context["signup_form"] = SignupForm()
        context["login_form"] = self.get_form(self.form_class)
        return context


class SignupView(RedirectToSigninOrHomeMixin, FormView):
    """
    Signup endpoint: processes the signup form and signs the user up (and logs
    them in). Note that the sign up with facebook functionality is entirely
    different: this is only for the regular django auth signup flow.

    Http verbs:
        GET: redirect to signin page
        POST: check post params against form, redirect to signin page if the
            form is not valid.
    """
    form_class = SignupForm
    template_name = "base/sign_in.html"

    def form_valid(self, form):
        form.save()
        # log in the newly created user model. if there is a problem, error
        auth_login(self.request, form.ensure_authenticated_user())
        messages.success(self.request, 'Signed up successfully!')
        return redirect("home")

    def get_context_data(self, *args, **kwargs):
        context = super(SignupView, self).get_context_data(**kwargs)
        context["signup_form"] = self.get_form(self.form_class)
        context["login_form"] = AuthenticationForm()
        return context


class LogoutView(UserDataMixin, View):
    """
    Basic logout view: Accessed whenever the user wants to logout, processes
    the logout, shows a toast, and redirects to home.
    """

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        messages.success(self.request, 'Logged out successfully')
        return redirect('home')
