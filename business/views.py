from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView

from wagtail.wagtaildocs.models import Document


class S3DocumentServe(RedirectView):
    """
    Temp redirect to S3 on document requests
    """
    def get_redirect_url(self, *args, **kwargs):
        document_id = kwargs['document_id']
        document = get_object_or_404(Document, id=document_id)
        return document.file.url
