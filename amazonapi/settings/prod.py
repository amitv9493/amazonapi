from .base import * 
DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATIC_ROOT = '/home/shipping/domains/shippingmart.co.uk/public_html/static'
