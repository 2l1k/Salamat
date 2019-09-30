
import re

from django import forms
from django.http import HttpResponse

from filesoup.base import InlineModelUploader, uploader_view

from baseapp.uploaders import RedactorUploaderMixin
from news.models import News, NewsImage


class BaseUploadForm(forms.ModelForm):
    """
    """
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(BaseUploadForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return super(BaseUploadForm, self).save(commit)


class NewsImageUploadForm(BaseUploadForm):
    class Meta:
        model = NewsImage
        exclude = ()


class AdminNewsImageUploader(RedactorUploaderMixin, InlineModelUploader):
    """
    Photo uploader for Model admin.
    """
    max_file_size = 8000000  # 8MB max.
    max_num = None
    form = NewsImageUploadForm

    class Widget:
        thumbnail_css_class = 'thumbnail fresco'
        jquery = False

    model = NewsImage
    parent_model = News
    use_model_upload_to = True

    news_edit_re = re.compile(r'news-(\d+)/')

    @classmethod
    def get_init_kwargs(cls, request, args, kwargs):
        init_kwargs = super(AdminNewsImageUploader, cls).get_init_kwargs(
            request, args, kwargs)

        # Determine current model.
        news = None
        match = cls.news_edit_re.search(request.path)
        if match:
            news_pk = match.group(1)
            try:
                news = News.objects.get(pk=news_pk)
            except news.DoesNotExist:
                pass
            else:
                init_kwargs['instance'] = news

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
