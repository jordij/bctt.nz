from .base import *
import dj_database_url
import os

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = False

# Compress static files offline
BASE_DIR = os.path.abspath(os.path.dirname(__name__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch.ElasticSearch',
        'INDEX': SITE_NAME,
    },
}

# Use the cached template loader
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': SITE_NAME,
    }
}

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
