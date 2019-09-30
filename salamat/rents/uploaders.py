
import re

from django import forms
from django.http import HttpResponse

from filesoup.base import InlineModelUploader, uploader_view

from baseapp.uploaders import RedactorUploaderMixin
from rents.models import Rent, RentsImage


class BaseUploadForm(forms.ModelForm):
    """
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(BaseUploadForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return super(BaseUploadForm, self).save(commit)





class RentsImageUploadForm(BaseUploadForm):
    class Meta:
        model = RentsImage
        exclude = ()


class AdminRentsImageUploader(RedactorUploaderMixin, InlineModelUploader):
    """
    Photo uploader for Model admin.
    """
    max_file_size = 8000000  # 8MB max.
    max_num = None
    form = RentsImageUploadForm

    class Widget:
        thumbnail_css_class = 'thumbnail fresco'
        jquery = False

    model = RentsImage
    parent_model = Rent
    use_model_upload_to = True

    rents_edit_re = re.compile(r'rents-(\d+)/')

    @classmethod
    def get_init_kwargs(cls, request, args, kwargs):
        init_kwargs = super(AdminRentsImageUploader, cls).get_init_kwargs(
            request, args, kwargs)

        # Determine current model.
        rents = None
        match = cls.rents_edit_re.search(request.path)
        if match:
            rents_pk = match.group(1)
            try:
                rents = Rent.objects.get(pk=rents_pk)
            except rents.DoesNotExist:
                pass
            else:
                init_kwargs['instance'] = rents

        return init_kwargs

    def get_form_kwargs(self, i):
        """
        Pass a request in order to request.user become available in a form.
        """
        return dict(request=self.request)

    @uploader_view(r'setup\.js$')
    def setup_js(self):
        """
        Additional script for Redactor.js integration.
        """
        script = """
        Salamat.contextData.redactorOptions = {imageGetJson: '%s'};
        """
        script %= self.reverse('redactor_files', args=(self.namespace,
                                                       self.prefix))
        return HttpResponse(script, content_type='text/javascript')
