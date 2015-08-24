from .base import *
import djcelery
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE

COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

# Static folder ready for production mode
STATIC_ROOT = join(DJANGO_ROOT, 'static')
STATICFILES_DIRS = ()

# Add apps
INSTALLED_APPS += (
    'djcelery',
)

ALLOWED_HOSTS = ['*']

# Celery

djcelery.setup_loader()
# Enables error emails.
CELERY_SEND_TASK_ERROR_EMAILS = True

BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Use Elasticsearch as the search backend for extra performance and better search results:
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#search
# http://wagtail.readthedocs.org/en/latest/core_components/search/backends.html#elasticsearch-backend

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': SITE_NAME,
    },
}

# Use Redis as the cache backend for extra performance

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
        'KEY_PREFIX': SITE_NAME,
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        }
    }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
) + MIDDLEWARE_CLASSES + (
    'django.middleware.cache.FetchFromCacheMiddleware',
)

# Make sure we include the needed Middleware apps
# Excluding logged in (admin) requests
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass
