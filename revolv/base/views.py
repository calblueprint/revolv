from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView, View
from django.core.urlresolvers import reverse
from revolv.base.forms import SignupForm
from revolv.base.users import UserDataMixin
from revolv.base.utils import ProjectGroup
from revolv.payments.models import Payment
from revolv.project.models import Project, Category
from revolv.project.utils import aggregate_stats

class HomePageView(UserDataMixin, TemplateView):
    """
    Website home page.

    TODO: this view is deprecated - most of the context variables are not
    used anymore. Should be cleaned up.
    """
    template_name = 'base/home.html'
    NUM_PROJECTS_SHOWN = 1000

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        active = Project.objects.get_active()
        context["first_project"] = active[0] if active.count() > 0 else None
        context["featured_projects"] = Project.objects.get_featured(
            HomePageView.NUM_PROJECTS_SHOWN)
        context["completed_projects_count"] = Project.objects.get_completed().count()
        context["total_donors_count"] = Payment.objects.total_distinct_organic_donors()
        return context


class BaseStaffDashboardView(UserDataMixin, TemplateView):
    """
    Base view for the administrator and ambassador dashboard views. The
    specific views in administrator/views.py and ambassador/views.py
    will inherit from this view.
    """

    def get_filter_args(self):
        """
        Return an array of arguments to pass to Project.objects.get_[drafted|proposed|active|completed].
        """
        return []

    def get_context_data(self, **kwargs):
        context = super(BaseStaffDashboardView, self).get_context_data(**kwargs)

        project_dict = {}
        project_dict[ProjectGroup('Proposed Projects', "proposed")] = Project.objects.get_proposed(*self.get_filter_args())
        project_dict[ProjectGroup('Active Projects', "active")] = Project.objects.get_active(*self.get_filter_args())
        project_dict[ProjectGroup('Completed Projects', "completed")] = Project.objects.get_completed(*self.get_filter_args())

        context["project_dict"] = project_dict
        context["role"] = self.role or "donor"

        context['donated_projects'] = Project.objects.donated_projects(self.user_profile)
        statistics_dictionary = aggregate_stats(self.user_profile)
        context['statistics'] = statistics_dictionary

        context['category_setter_url'] = reverse('dashboard_category_setter')
        context['categories'] = Category.objects.all().order_by('title')
        context['preferred_categories'] = self.user_profile.preferred_categories.all()

        # TODO (noah): add in support for autoshowing a project based on the active_project GET parameter
        return context

class CategoryPreferenceSetterView(UserDataMixin, View):
    
    http_methods = ['post']
    
    def http_method_not_allowed(request, *args, **kwargs):
        return redirect("dashboard")

    def post(self, request, *args, **kwargs):
        user = self.user_profile
        user.preferred_categories.clear()
        info_dict = request.POST.dict()
        for category_string in info_dict:
            category = Category.objects.get(id=category_string)
            user.preferred_categories.add(category)
        return HttpResponse()

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
        context["referring_endpoint"] = ""
        context["reason"] = self.request.GET.get("reason")
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
    url_append = "#login"
    redirect_view = "signin"

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
        context["referring_endpoint"] = "login"
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
    url_append = "#signup"
    redirect_view = "signin"

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
        context["referring_endpoint"] = "signup"
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


class DashboardRedirect(UserDataMixin, View):
    """
    Redirects user to appropriate dashboard. (e.g. Administrators automagically
    go to the /dashboard/admin endpoint)

    Redirects to home page if not authenticated.
    """

    def get(self, request, *args, **kwargs):
        if not self.is_authenticated:
            return redirect('home')
        if self.is_administrator:
            return redirect('administrator:dashboard')
        if self.is_ambassador:
            return redirect('ambassador:dashboard')
        return redirect('donor:dashboard')


# password reset/change views: thin wrappers around django's built in password
# reset views, but with our own templates
def password_reset_initial(request):
    return auth_views.password_reset(
        request,
        template_name="base/auth/forgot_password_initial.html",
        email_template_name="base/auth/forgot_password_email.html",
        from_email="support@re-volv.org"
    )


def password_change(request):
    return auth_views.password_change(
        request,
        template_name="base/auth/change_password.html",
        post_change_redirect="/dashboard/donor/?password_change_success",
    )


def password_reset_done(request):
    return auth_views.password_reset_done(request, template_name="base/auth/forgot_password_done.html")


def password_reset_confirm(request, *args, **kwargs):
    kwargs.update({"template_name": "base/auth/forgot_password_confirm.html"})
    return auth_views.password_reset_confirm(request, *args, **kwargs)


def password_reset_complete(request):
    return auth_views.password_reset_complete(request, template_name="base/auth/forgot_password_complete.html")
