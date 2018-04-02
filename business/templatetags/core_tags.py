from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from wagtail.wagtailcore.rich_text import expand_db_html

from business.snippets import NavigationMenu, Sponsor
from business.utilities import *

register = template.Library()


@register.inclusion_tag('business/includes/header.html', takes_context=True)
def menu(context, name=None, current_page=None):
    """
    Retrieves the MenuElement(s) under the NavigationMenu with given menu_name
    """
    if name is None or current_page is None:
        return None
    try:
        menu_items = NavigationMenu.objects.get(menu_name=name).items

        if current_page:
            for item in menu_items:
                if item.link_page:
                    if item.link_page.id == current_page.id or current_page.is_descendant_of(item.link_page):
                        item.is_active = True
    except ObjectDoesNotExist:
        return None

    return {
        'links': menu_items,
        'request': context['request'],
    }


@register.inclusion_tag('business/includes/footer_menu.html')
def footer_menu(name=None):
    """
    Retrieves the MenuElement(s) under the NavigationMenu with given menu_name
    """
    if name is None:
        return None
    try:
        menu_items = NavigationMenu.objects.get(menu_name=name).items
    except ObjectDoesNotExist:
        return None

    return {
        'title': name,
        'links': menu_items,
    }


@register.inclusion_tag('business/includes/sponsors.html', takes_context=True)
def sponsors_menu(context, current_page=None):
    """
    Retrieves the sponsors
    """
    if hasattr(current_page, 'sponsors'):
        sponsors = current_page.sponsors
    else:
        sponsors = Sponsor.objects.filter(regions=None)
    return {
        'sponsors': sponsors,
    }
