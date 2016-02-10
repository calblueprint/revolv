import sys

from revolv.settings.base import *  # noqa

DEBUG = True
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

#INSTALLED_APPS += (
#    'debug_toolbar',
#)

INTERNAL_IPS = ('127.0.0.1', )

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CELERY_ALWAYS_EAGER = True

CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

SECRET_KEY = os.environ.get('SECRET_KEY', 'uypx8s@%0u6in(7a=7v2m_w%*y^yo+a)_=45x*gib-e_vl^zm_')

# Special test settings
if 'test' in sys.argv:
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    LOGGING['root']['handlers'] = []
