from django.db import models

from wagtail.wagtailforms.models import AbstractFormField, AbstractEmailForm
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.fields import ParentalKey


class SubmitFormField(AbstractFormField):
    page = ParentalKey('SubmitFormPage', related_name='form_fields')


class SubmitFormPage(AbstractEmailForm):
    """
    Form page, inherits from SweetCaptchaEmailForm if available, otherwise fallback to AbstractEmailForm
    """
    subpage_types = []
    search_fields = ()
    thank_you_text = RichTextField(blank=True, help_text='Set the message users will see after submitting the form.')
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    subtitle = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Contact form"
        description = "Page with a contact form"


SubmitFormPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('subtitle', classname="full"),
    FieldPanel('thank_you_text', classname="full"),
    InlinePanel(SubmitFormPage, 'form_fields', label="Form fields"),
    MultiFieldPanel([
        FieldPanel('to_address'),
        FieldPanel('from_address'),
        FieldPanel('subject'),
    ], "Email notification")
]

SubmitFormPage.promote_panels = AbstractEmailForm.promote_panels + [
    ImageChooserPanel('feed_image'),
]
