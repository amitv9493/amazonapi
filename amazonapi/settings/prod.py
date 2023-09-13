from .base import * 
DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': os.environ.get('db_name'),
        'USER': os.environ.get('user'),
        'PASSWORD': os.environ.get('password'),
        'HOST': '69.10.43.179',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

STATIC_URL = "static/"
MEDIA_URL = "media/"

STATIC_ROOT = '/home/shipping/domains/shippingmart.co.uk/public_html/static'
