"""
Django settings for revolv project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('RE-volv Team', 'kmtracey@caktusgroup.com'),
)

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',

    # revolv apps
    'revolv.base',
    'revolv.project',
    'revolv.administrator',
    'revolv.ambassador',
    'revolv.donor',
    'revolv.payments',

    # 3rd-party apps
    'django_facebook',
    'storages',
    'imagekit',
    'widget_tweaks',
    'djcelery',
    'ckeditor',
    'sekizai',
    'social.apps.django_app.default',

    # wagtail cms: see http://wagtail.readthedocs.org/en/v1.0b2/howto/settings.html
    'compressor',
    'taggit',
    'modelcluster',
    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailredirects',
    'wagtailsettings',
    'revolv.revolv_cms'
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    'sesame.middleware.AuthenticationMiddleware',
    'revolv.base.users.RevolvSocialAuthExceptionMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'sesame.backends.ModelBackend',
]

ROOT_URLCONF = 'revolv.urls'

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
]
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'django_facebook.context_processors.facebook',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'sekizai.context_processors.sekizai',
    'wagtailsettings.context_processors.settings',
]

WSGI_APPLICATION = 'revolv.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'revolv',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

if os.path.exists("/dev/log"):
    SYSLOG_PATH = "/dev/log"
else:
    SYSLOG_PATH = "/var/run/syslog"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'basic': {
            'format': '%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
        },
        'papertrail': {
            'format': 'django %(asctime)s %(name)s %(levelname)s: %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'address': SYSLOG_PATH,
            'facility': 'local6',
            'filters': ['require_debug_false'],
            'formatter': 'papertrail',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'syslog'],
        'level': 'INFO',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'locale'), )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'  # for the {% compress %} tags in wagtail to work
)

# If using Celery, tell it to obey our logging configuration.
CELERYD_HIJACK_ROOT_LOGGER = False

# https://docs.djangoproject.com/en/1.9/topics/auth/passwords/#password-validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Make things more secure by default. Run "python manage.py check --deploy"
# for even more suggestions that you might want to add to the settings, depending
# on how the site uses SSL.
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

## Additional settings for RE-volv

# disable django-compressor for wagtail admin pages. this is hacky
# but necessary until we can get it to play nicer with s3.
# see https://github.com/calblueprint/revolv/issues/363
COMPRESS_ENABLED = False

CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

WAGTAIL_SITE_NAME = 'RE-volv'
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'content-management-bot@re-volv.org'

# Login settings
LOGIN_URL = '/signin'

import djcelery
from celery.schedules import crontab

from datetime import datetime

# import celery for scheduled tasks
djcelery.setup_loader()

EMAIL_TEMPLATES_PATH = os.path.join(
    BASE_DIR,
    'templates',
    'emails',
    'emails.yml'
)

# TODO: FIX THIS
# Hard-coded urls: kind of ugly but we need these for when we
# want to send links in emails
SITE_URL = os.environ.get('SITE_URL', 'http://revolv.local.com:8000')

#username admin will assign when automatic reinvest task run
ADMIN_PAYMENT_USERNAME = 'administrator'
#date of the month when user can execute reinvest
USER_REINVESTMENT_DATE = {'day': 1, 'hour': 00, 'minute': 00}
#date of the month when automatic reinvest execute
ADMIN_REINVESTMENT_DATE = {'day': 15, 'hour': 00, 'minute': 00}

now = datetime.now()
#Datetime object when automatic reinvest run, we need to increase a little to prevent overlap with user reinvestment
ADMIN_REINVESTMENT_DATE_DT = datetime(now.year, now.month, **ADMIN_REINVESTMENT_DATE)

# The backend used to store task results - because we're going to be
# using RabbitMQ as a broker, this sends results back as AMQP messages
CELERY_RESULT_BACKEND = "amqp"

CELERY_IMPORTS = ('revolv.tasks.reinvestment_allocation', 'revolv.tasks.reinvestment_rollover',)
# The default Django db scheduler
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_SCHEDULE = {
    "scrape": {
        "task": "revolv.project.tasks.scrape",
        # Every Sunday at 4:30AM
        "schedule": crontab(hour=4, minute=30, day_of_week=0),
        "args": (2, 4),

    },
    "reinvestment_allocation": {
        "task": "revolv.tasks.reinvestment_allocation.calculate_montly_reinvesment_allocation",
        "schedule": crontab(hour=USER_REINVESTMENT_DATE['hour'], minute=USER_REINVESTMENT_DATE['minute'],
                            day_of_month=USER_REINVESTMENT_DATE['day']),
    },
    "reinvestment_rollover": {
        "task": "revolv.tasks.reinvestment_rollover.distribute_reinvestment_fund",
        "schedule": crontab(hour=ADMIN_REINVESTMENT_DATE['hour'], minute=ADMIN_REINVESTMENT_DATE['minute'],
                            day_of_month=ADMIN_REINVESTMENT_DATE['day']),
    }
}

GOOGLEMAPS_API_KEY = "AIzaSyDVDPi1SXm3qKyvmE5i9XeO1Gs5WjK7SJE"

LANGUAGES = [
    ('en-us', 'English'),
]

# Facebook app keys
# TODO: determine if these 2 are needed. They are not set in the
# existing Heroku app environment, so I can't pull them to new box.
FACEBOOK_APP_ID = os.environ.get("REVOLV_FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.environ.get("REVOLV_FACEBOOK_APP_SECRET")

SOCIAL_AUTH_URL_NAMESPACE = 'social'

"""
Payment Charging is enabled by default.

When in developement, payments go to the Paypal Sandbox. This (should) mean
that no cards are actually being charged; they just show up in the PayPal
dashboard so that you can run tests, track payments, etc.

On production, payments go to the actual Paypal account, meaning that cards
actually do get charged.

Consequently, it's safe to always enable charging, since in development nothing
is actually being charged on the PayPal side.
"""
ENABLE_PAYMENT_CHARGING = True

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'revolv.base.users.get_username_from_social',
    'social.pipeline.social_auth.associate_by_email',
    'revolv.base.users.create_user_revolv',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect'
)

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email'}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['profile', 'email']

SOCIAL_AUTH_LOGIN_ERROR_URL = '/social_connect_failed/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'first_name', 'last_name']

# TODO: determine if this value is needed and if so what it should be
# (This values does not exist in Heroku environment.)
SHARETHIS_PUBLISHER_ID = os.environ.get('SHARETHIS_PUBLISHER_ID')

# Salesforce TODO: obtain these account values
SFDC_ACCOUNT = os.environ.get('SFDC_ACCOUNT')
SFDC_PASSWORD = os.environ.get('SFDC_PASSWORD')
SFDC_TOKEN = os.environ.get('SFDC_TOKEN')

SFDC_REVOLV_SIGNUP = 'login'
SFDC_REVOLV_DONATION = 'donation'

#Stripe
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE = os.environ.get('STRIPE_PUBLISHABLE')
