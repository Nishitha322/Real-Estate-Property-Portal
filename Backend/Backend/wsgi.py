"""WSGI config for the Real Estate Property Portal backend."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")

application = get_wsgi_application()
