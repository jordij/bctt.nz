from .base import *

# Analytics stuff
GOOGLE_TAG_MANAGER = False
GOOGLE_ANALYTICS_KEY = False

DEBUG = True
TEMPLATE_DEBUG = True

COMPRESS_ENABLED = False

DATABASES['default']['PASSWORD'] = ''

# To have fake email backend

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += (
    'wagtail.contrib.wagtailstyleguide',
)

CACHE_MIDDLEWARE_SECONDS = 0

RECAPTCHA_PUBLIC_KEY = 'set_your_key'
RECAPTCHA_PRIVATE_KEY = 'set_your_key'
NOCAPTCHA = True