from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from wagtail.wagtailcore.rich_text import expand_db_html

from business.snippets import NavigationMenu, Sponsor
from business.utilities import *

register = template.Library()


@register.filter
def raw(value):
    if value is not None:
        html = expand_db_html(value)
    else:
        html = ''

    return mark_safe(html)


@register.filter
def content_type(model):
    """
    Return the model name/"content type" as a string e.g BlogPage, NewsListingPage.
    Can be used with "slugify" to create CSS-friendly classnames
    Usage: {% raw %}{{ self|content_type|slugify }} {% endraw %}
    """
    return model.__class__.__name__


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
                if item.link_page and item.link_page.id == current_page.id or current_page.is_descendant_of(item.link_page):
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


@register.inclusion_tag('business/includes/sponsors.html')
def sponsors_menu():
    """
    Retrieves all the sponsors
    """
    sponsors = Sponsor.objects.all()

    return {
        'sponsors': sponsors,
    }


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


@register.tag(name='set')
def set_var(parser, token):
    """
    Usage: {% set var_name  = var_value %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set var_name = var_value %}")
    return SetVarNode(parts[1], parts[3])
