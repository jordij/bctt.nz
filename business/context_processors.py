from django.conf import settings


def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    ga_key = getattr(settings, 'GOOGLE_ANALYTICS_KEY', False)
    ga_tag = getattr(settings, 'GOOGLE_TAG_MANAGER', False)

    if ga_key:
        return {
            'GOOGLE_ANALYTICS_KEY': ga_key,
            'GOOGLE_TAG_MANAGER': ga_tag,
        }
    return {}
