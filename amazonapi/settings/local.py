from .base import *
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "static/"


INSTALLED_APPS += ["django_extensions"]



REST_FRAMEWORK = {
    "DEFAULT_RESPONSE_CLASS": "rest_framework.response.JSONResponse",
}