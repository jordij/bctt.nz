from django.conf import settings


def has_recaptcha():
    """
    Check if the WagtailCaptcha settings are properly set
    """
    wagtailcaptcha_public_key = getattr(settings, 'RECAPTCHA_PUBLIC_KEY', None)
    wagtailcaptcha_private_key = getattr(settings, 'RECAPTCHA_PRIVATE_KEY', None)
    return wagtailcaptcha_public_key and wagtailcaptcha_private_key
