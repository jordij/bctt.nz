import json

from wagtail.wagtailcore.whitelist import Whitelister, attribute_rule, check_url
from wagtail.wagtailcore.fields import RichTextArea

allow_without_attributes = attribute_rule({})


# Simple TextArea, where we nee just a few options on editor
class SimpleDbWhitelister(Whitelister):
    element_rules = {
        '[document]': allow_without_attributes,
        'a': attribute_rule({'href': check_url}),
        'p': allow_without_attributes,
        'b': allow_without_attributes,
        'i': allow_without_attributes,
        'u': allow_without_attributes,
        'h2': allow_without_attributes,
    }


class SimpleRichTextArea(RichTextArea):
    hallo_plugins = {
        'halloheadings': {
            'formatBlocks': ['p', 'h2']
        },
        'halloformat': {
            'formattings': {
                "bold": True,
                "italic": True,
            },
        },
        'hallowagtaildoclink': {},
        'hallolists': {
            "lists": {
                "ordered": True,
                "unordered": True
            }
        },
        'hallowagtaillink': {},
        'hallorequireparagraphs': {},
        'hallocleanhtml': {
            'format': False,
            'removeTags': ['span', 'div', 'table', 'strong'],
            'allowedTags': ['a', 'p', 'i', 'b', 'u'],
            'removeAttrs': ['class', 'style', 'id'],
            'allowedAttributes': [
                ["a", ['href', 'target', 'data-id', 'data-linktype']]
            ]
        }
    }

    def render_js_init(self, id_, name, value):
        return "makeRichTextEditable({0}, {1});".format(
            json.dumps(id_),
            json.dumps(self.hallo_plugins)
        )

    def value_from_datadict(self, data, files, name):
        original_value = super(SimpleRichTextArea, self).value_from_datadict(data, files, name)
        if original_value is None:
            return None
        return SimpleDbWhitelister.clean(original_value)
