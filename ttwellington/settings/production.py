import dj_database_url
import os
from memcacheify import memcacheify

from .base import *


GOOGLE_ANALYTICS_KEY = 'UA-24461191-2'

NOCAPTCHA = True

INSTALLED_APPS += (
   'herokuapp',
)

# Heroku platform settings.
HEROKU_APP_NAME = "bctt"
HEROKU_BUILDPACK_URL = "https://github.com/heroku/heroku-buildpack-python.git"
SITE_DOMAIN = "bctt.herokuapp.com"

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

RECAPTCHA_PUBLIC_KEY = env['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = env['RECAPTCHA_PRIVATE_KEY']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Allow domain host headers
ALLOWED_HOSTS = [
    'bctt.nz',
    'www.bctt.nz',
    'bctt.herokuapp.com',
    'www.bctt.herokuapp.com',
    'bctt.herokudns.com',
    'www.bctt.herokudns.com',
]

# Sendgrid Email settings
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = env['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = env['SENDGRID_PASSWORD']
EMAIL_PORT = 25
EMAIL_USE_TLS = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

BASE_DIR = os.path.abspath(os.path.dirname(__name__))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Use Amazon S3 for storage for uploaded media files.
DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"

# Use Amazon S3 for static files storage.
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
# "require_s3.storage.OptimizedCachedStaticFilesStorage"
STATIC_ROOT = 'staticfiles'

# Amazon S3 settings.
AWS_ACCESS_KEY_ID = env['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = env['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = env['AWS_STORAGE_BUCKET_NAME']
AWS_AUTO_CREATE_BUCKET = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
COMPRESS_URL = STATIC_URL
MEDIA_URL = "https://%s/media/" % AWS_S3_CUSTOM_DOMAIN

AWS_S3_FILE_OVERWRITE = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = True
AWS_IS_GZIPPED = False

CACHES = memcacheify()

# Compress static files offline
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db',
        'AUTO_UPDATE': True,
    }
}

# Use the cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
) + MIDDLEWARE_CLASSES + (
    'django.middleware.cache.FetchFromCacheMiddleware',
)

# Excluding logged in (admin) requests
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
