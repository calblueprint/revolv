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
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django_facebook.context_processors.facebook',
)

SITE_ID = 1

# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style',  # must go before 'django.contrib.admin'.

    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'djangobower',
    'django.contrib.humanize',

    # revolv apps
    'revolv.base',
    'revolv.project',
    'revolv.administrator',
    'revolv.ambassador',
    'revolv.donor',
    'revolv.payments',

    # vendor apps
    'django_facebook',
    'storages',
    'imagekit',
    'widget_tweaks',
    'djcelery',
    'ckeditor',

    # django-cms
    'wagtail'
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
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
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
CMS_TEMPLATES = (
    ('base/cms_templates/template_1.html', 'Template One'),
)
CMS_PERMISSION = True
CMS_PUBLIC_FOR = "staff"

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    'sekizai.context_processors.sekizai',
    'cms.context_processors.cms_settings',
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

# Static asset configuration
STATIC_ROOT = 'staticfiles'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)

# djangobower settings
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')
BOWER_INSTALLED_APPS = (
    'foundation',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = os.environ.get('REVOLV_AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('REVOLV_AWS_SECRET_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('REVOLV_S3_BUCKET', '')

S3_URL = 'http://%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIA_DIRECTORY = '/media/'
MEDIA_URL = S3_URL + MEDIA_DIRECTORY

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

# Allow all host headers
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

# django-cms
MIGRATION_MODULES = {
    'cms': 'cms.migrations_django',
    'menus': 'menus.migrations_django',
    'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
    'djangocms_picture': 'djangocms_picture.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_file': 'djangocms_file.migrations_django',
    'djangocms_video': 'djangocms_video.migrations_django',
}

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
