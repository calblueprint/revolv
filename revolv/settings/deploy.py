# Settings for live deployed environments: vagrant, staging, production, etc
from .base import *  # noqa

os.environ.setdefault('CACHE_HOST', '127.0.0.1:11211')
os.environ.setdefault('BROKER_HOST', '127.0.0.1:5672')

ENVIRONMENT = os.environ['ENVIRONMENT']

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['NAME'] = 'revolv_%s' % ENVIRONMENT.lower()
DATABASES['default']['USER'] = 'revolv_%s' % ENVIRONMENT.lower()
DATABASES['default']['HOST'] = os.environ.get('DB_HOST', '')
DATABASES['default']['PORT'] = os.environ.get('DB_PORT', '')
DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD', '')

WEBSERVER_ROOT = '/var/www/revolv/'

PUBLIC_ROOT = os.path.join(WEBSERVER_ROOT, 'public')

STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')

MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'media')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%(CACHE_HOST)s' % os.environ,
    }
}

EMAIL_SUBJECT_PREFIX = '[Revolv %s] ' % ENVIRONMENT.title()
DEFAULT_FROM_EMAIL = 'info@re-volv.org'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

ALLOWED_HOSTS = [os.environ['DOMAIN']]

# Use template caching on deployed servers
""" Requires Django 1.8 which wer don't have yet
for backend in TEMPLATES:
    if backend['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
        default_loaders = ['django.template.loaders.filesystem.Loader']
        if backend.get('APP_DIRS', False):
            default_loaders.append('django.template.loaders.app_directories.Loader')
            # Django gets annoyed if you both set APP_DIRS True and specify your own loaders
            backend['APP_DIRS'] = False
        loaders = backend['OPTIONS'].get('loaders', default_loaders)
        for loader in loaders:
            if len(loader) == 2 and loader[0] == 'django.template.loaders.cached.Loader':
                # We're already caching our templates
                break
        else:
            backend['OPTIONS']['loaders'] = [('django.template.loaders.cached.Loader', loaders)]
"""

# Uncomment if using celery worker configuration
CELERY_SEND_TASK_ERROR_EMAILS = True
BROKER_URL = 'amqp://revolv_%(ENVIRONMENT)s:%(BROKER_PASSWORD)s@%(BROKER_HOST)s/revolv_%(ENVIRONMENT)s' % os.environ  # noqa

# Environment overrides
# These should be kept to an absolute minimum
if ENVIRONMENT.upper() == 'LOCAL':
    # Don't send emails from the Vagrant boxes
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
