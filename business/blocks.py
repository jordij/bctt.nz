from django import forms
from django.utils.functional import cached_property

from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import RichTextBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


class SimpleRichTextBlock(RichTextBlock):
    class Meta:
        icon = 'bold'


class QuoteBlock(blocks.StructBlock):
    """
    Block for rich text quotes
    """
    quote = blocks.CharBlock(required=True)
    author = blocks.CharBlock(required=False)
    author_title = blocks.CharBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = 'openquote'
        template = 'business/blocks/quote_block.html'


class CaptionImageBlock(blocks.StructBlock):
    """
    Block for images
    """
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'business/blocks/caption_image_block.html'
