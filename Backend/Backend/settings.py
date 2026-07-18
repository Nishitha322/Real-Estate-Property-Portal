"""
Django settings for the Real Estate Property Portal backend.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-insecure-key-change-me-in-production"
)

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "corsheaders",
    "portal",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "Backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.parent / "Frontend",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "Backend.wsgi.application"

DATABASES = {}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR.parent / "Frontend",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://krishnadarapaneni85_db_user:KRISHNA%40681d@cluster0.63tdiai.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
)

MONGO_DB_NAME = os.environ.get(
    "MONGO_DB_NAME",
    "realestate_portal",
)