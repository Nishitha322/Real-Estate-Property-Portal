"""
ASGI config for the Real Estate Property Portal backend.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Backend.settings")

application = get_asgi_application()
