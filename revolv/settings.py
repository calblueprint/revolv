"""
Django settings for revolv project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

import dj_database_url
import djcelery
from celery.schedules import crontab

# If you'd like to possibly receive error status emails, add yourself
# to this list:
ADMINS = (
    #("Noah Gilmore", "noah.w.gilmore@gmail.com"),
    ("Philip Neustrom", "philipn+revolv@gmail.com"),
)

# import celery for scheduled tasks
djcelery.setup_loader()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.dirname(os.path.realpath(__file__))

IS_STAGE = 'IS_STAGE' in os.environ
IS_PROD = 'IS_PROD' in os.environ
IS_HEROKU = IS_STAGE or IS_PROD
IS_LOCAL = not IS_HEROKU

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "REVOLV_SECRET_KEY",
    "mysecretkeyshhhguysitsasecret"
)

# Facebook app keys
FACEBOOK_APP_ID = os.environ.get("REVOLV_FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.environ.get("REVOLV_FACEBOOK_APP_SECRET")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = IS_LOCAL
# disable django-compressor for wagtail admin pages. this is hacky
# but necessary until we can get it to play nicer with s3.
# see https://github.com/calblueprint/revolv/issues/363
COMPRESS_ENABLED = False

TEMPLATE_DEBUG = IS_LOCAL

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangobower',
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
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'revolv.urls'

WSGI_APPLICATION = 'revolv.wsgi.application'

# Templates

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

WAGTAIL_SITE_NAME = 'RE-volv'
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'content-management-bot@re-volv.org'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django_facebook.context_processors.facebook',

    'sekizai.context_processors.sekizai',
    'wagtailsettings.context_processors.settings',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'revolv_db',
        'USER': 'revolv',
        'PASSWORD': 'revolv',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

if IS_HEROKU:
    DATABASES['default'] = dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True


# Login settings
LOGIN_URL = '/signin'

AWS_ACCESS_KEY_ID = os.environ.get('REVOLV_AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('REVOLV_AWS_SECRET_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('REVOLV_S3_BUCKET', '')

# Default media file (uploads) storage on Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

S3_URL = 'https://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIA_PATH = '/media/'
MEDIA_URL = S3_URL + MEDIA_PATH

MEDIA_SERVE_LOCALLY = False
if not AWS_ACCESS_KEY_ID and IS_LOCAL:
    # Local developer hasn't gotten our official AWS keys, so let's
    # allow them to 
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = MEDIA_PATH
    MEDIA_SERVE_LOCALLY = False

STATIC_ROOT = 'staticfiles'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder'  # for the {% compress %} tags in wagtail to work
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

if IS_LOCAL:
    # On local, we use django's built in static files app, which will serve
    # static files (css, js, etc) directly from the project directory called
    # "static" (that directory is a sibling of this file in the directory tree)
    # See https://docs.djangoproject.com/en/1.7/howto/static-files/
    STATIC_URL = '/static/'
else:
    # on staging/production, we use Amazon S3 for storage.
    # See https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

    # the bucket directory in which to collect static files for staging
    STATICFILES_STAGING_LOCATION = "static_staging"
    # the corresponding bucket directory for static files on prod
    STATICFILES_PRODUCTION_LOCATION = "static_production"
    if IS_PROD:
        staticfiles_location = STATICFILES_PRODUCTION_LOCATION
        STATICFILES_STORAGE = 'revolv.custom_storages.RevolvProductionStaticStorage'
    else:
        staticfiles_location = STATICFILES_STAGING_LOCATION
        STATICFILES_STORAGE = 'revolv.custom_storages.RevolvStagingStaticStorage'
    STATIC_URL = "%s/%s/" % (S3_URL, staticfiles_location)

# djangobower settings
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')
BOWER_INSTALLED_APPS = (
    'foundation',
)

# email settings
# see http://stackoverflow.com/questions/9723494/setting-up-email-with-sendgrid-in-heroku-for-a-django-app
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "team@re-volv.org"
if IS_HEROKU:
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_HOST_USER = os.environ["SENDGRID_USERNAME"]
    EMAIL_HOST_PASSWORD = os.environ["SENDGRID_PASSWORD"]
else:
    EMAIL_HOST = "localhost"
    EMAIL_HOST_USER = "revolv@localhost.org"  # doesn't matter on local
    EMAIL_HOST_PASSWORD = ""

EMAIL_TEMPLATES_PATH = os.path.join(
    SETTINGS_PATH,
    'templates',
    'emails',
    'emails.yml'
)

# Hard-coded urls: kind of ugly but we need these for when we
# want to send links in emails
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')

if IS_HEROKU:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Heroku Settings
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow host headers only for our actual sites - see
# https://docs.djangoproject.com/en/1.7/ref/settings/#allowed-hosts
if IS_PROD:
    ALLOWED_HOSTS = ["revolv-prod.herokuapp.com", ".re-volv.org"]
elif IS_STAGE:
    ALLOWED_HOSTS = ["revolv-stage.herokuapp.com", "revolv-test-site.herokuapp.com"]
else:
    ALLOWED_HOSTS = ['*']

# The backend used to store task results - because we're going to be
# using RabbitMQ as a broker, this sends results back as AMQP messages
CELERY_RESULT_BACKEND = "amqp"
CELERY_ALWAYS_EAGER = True

# RabbitMQ broker settings
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_PASSWORD = "revolv"
BROKER_USER = "revolv"
BROKER_URL = "amqp://revolv:revolv@localhost:5672//revolv"

# The default Django db scheduler
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_SCHEDULE = {
    "scrape": {
        "task": "revolv.project.tasks.scrape",
        # Every Sunday at 4:30AM
        "schedule": crontab(hour=4, minute=30, day_of_week=0),
        "args": (2, 4),
    },
}

GOOGLEMAPS_API_KEY = "AIzaSyDVDPi1SXm3qKyvmE5i9XeO1Gs5WjK7SJE"

LANGUAGES = [
    ('en-us', 'English'),
]

# SSL Settings for Heroku
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SSLIFY_DISABLE = IS_LOCAL

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

# Used for error logging. See https://docs.djangoproject.com/en/1.7/topics/logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_facebook.models': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
}
