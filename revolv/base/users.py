from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.shortcuts import redirect
from revolv.base.models import RevolvUserProfile
from revolv.base.utils import get_profile

from social.apps.django_app.middleware import SocialAuthExceptionMiddleware


def is_ambassador(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in and an ambassador, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and get_profile(u).is_ambassador(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def is_administrator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in and an administrator, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and get_profile(u).is_administrator(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_logged_in(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in and an administrator, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class UserDataMixin(object):
    def deny_access(self):
        """Basic method to replace the default PermissionDenied()"""
        messages.error(
            self.request,
            'Oops! You do not have permission to access this page.'
        )
        return redirect('home')

    def deny_access_via_404(self, message):
        """Raise a 404 Not Found."""
        raise Http404(message)

    def dispatch(self, request, *args, **kwargs):
        """ dispatch() gets request.user and populates the view with relevant
        information, if applicable. If the user isn't logged in, then self.user
        is an AnonymousUser, which is a built-in Django user type. If the user
        is logged in, self.user is a django.contrib.auth.models.User.
        """
        self.user = request.user
        self.is_authenticated = self.user.is_authenticated()
        if self.is_authenticated:
            self.user_profile = RevolvUserProfile.objects.get(user=self.user)
            self.is_donor = self.user_profile.is_donor()
            self.is_ambassador = self.user_profile.is_ambassador()
            self.is_administrator = self.user_profile.is_administrator()
        else:
            self.user_profile = None
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


def get_username_from_social(strategy, details, user=None, *args, **kwargs):
    """
    Custom Social Auth pipeline to get username from email social account.
    First get username from email's user (without domain). If that name already been taken
    we'll use full email as username
    """
    USER_FIELDS = ['username', 'email']
    if 'username' not in strategy.setting('USER_FIELDS', USER_FIELDS):
        return

    storage = strategy.storage

    if not user:
        username, _ = details['email'].split('@')
        if storage.user.user_exists(username=username):
            username = details['email']
    else:
        username = storage.user.get_username(user)
    print {'username': username, 'details': details}
    return {'username': username}


class RevolvSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def get_redirect_uri(self, request, exception):
        message = self.get_message(request, exception)
        request.session['has_social_exception'] = True
        url = super(RevolvSocialAuthExceptionMiddleware, self).get_redirect_uri(request, exception)
        return '{0}?message={1}'.format(url, message)