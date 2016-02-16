"""
WSGI config for revolv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from . import load_env


load_env.load_env()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "revolv.settings")

application = get_wsgi_application()
