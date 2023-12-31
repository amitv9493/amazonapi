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

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '/home/shipping/.redis/redis.sock',
    },
}

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'



REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True


SESSION_COOKIE_SAMESITE = 'Lax'  # Adjust for development only
CSRF_COOKIE_SAMESITE = 'Lax'
# SESSION_COOKIE_DOMAIN = 'localhost:3000/'
CSRF_COOKIE_HTTPONLY =False
SESSION_COOKIE_HTTPONLY = False

# # PROD ONLY
# # CSRF_COOKIE_SECURE = True
# # SESSION_COOKIE_SECURE = True

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken', 'Set-Cookie']
CORS_ALLOW_CREDENTIALS = True