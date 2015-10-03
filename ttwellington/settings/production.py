from .base import *
import dj_database_url
import os


INSTALLED_APPS += (
   'herokuapp',
)

# Heroku platform settings.
HEROKU_APP_NAME = "wellyttbc"
HEROKU_BUILDPACK_URL = "https://github.com/heroku/heroku-buildpack-python.git"
SITE_DOMAIN = "wellyttbc.herokuapp.com"

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

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
STATICFILES_STORAGE = "require_s3.storage.OptimizedCachedStaticFilesStorage"
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
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False


# Cache settings.
def get_cache():
    try:
        os.environ['MEMCACHE_SERVERS'] = env['MEMCACHIER_SERVERS'].replace(',', ';')
        os.environ['MEMCACHE_USERNAME'] = env['MEMCACHIER_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = env['MEMCACHIER_PASSWORD']
        return {
          'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'TIMEOUT': 60 * 60 * 24,
            'BINARY': True,
            'OPTIONS': {'tcp_nodelay': True}
          }
        }
    except:
        return {
          'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
          }
        }

CACHES = get_cache()

# Compress static files offline

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'
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

# WAGTAILSEARCH_BACKENDS = {
#     'default': {
#         'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
#         'INDEX': SITE_NAME,
#     },
# }

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

try:
    from .local import *
except ImportError:
    pass
