
from django.contrib import admin
from django import forms
from django.forms import Media
from django.utils.translation import ugettext_lazy as _

from filesoup.forms import UploaderFormMixin
from filesoup.mixins import RequestProvidingModelAdminMixin
from baseapp.forms import RedactorWidget
from baseapp.helpers import get_assets
from news.models import News
from news.uploaders import AdminNewsImageUploader


class NewsAdminForm(UploaderFormMixin, forms.ModelForm):
    images = AdminNewsImageUploader.AdminFormField(label=_('Images'))

    class Meta:
        model = News
        fields = '__all__'

    # @property
    # def media(self):
    #     js = get_assets('lib_js', 'fresco_js')
    #     css = {'all': get_assets('fresco_css')}
    #
    #     uploader = self['images'].uploader
    #     redactor_js_url = uploader.reverse(
    #         'redactor_js', args=(uploader.namespace, uploader.prefix))
    #     js.append(redactor_js_url)
    #
    #     media = forms.Media(js=js, css=css)
    #     return media + super(NewsAdminForm, self).media

    def __init__(self, *args, **kwargs):
        super(NewsAdminForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = RedactorWidget(options={
            'fixed': True,
            'fixedBox': True
        })

    @property
    def media(self):
        js = get_assets('lib_js', 'fresco_js')
        js2 = []
        for s in js:
            js2.append(s.split('?', 1)[0])
        css = get_assets('fresco_css')

        css2 = []
        for s in css:
            css2.append(s.split('?', 1)[0])

        uploader = self['images'].uploader
        redactor_js_url = uploader.reverse(
            'redactor_js', args=(uploader.namespace, uploader.prefix))
        js2.append(redactor_js_url)
        return Media(js=js2, css={'all': css2}) + super(NewsAdminForm, self).media


class NewsAdmin(RequestProvidingModelAdminMixin, admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'active')

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(NewsAdmin, self).get_form(request, obj=None, **kwargs)
    #     form.base_fields['description'].widget = RedactorWidget(options={
    #         'fixed': True,
    #         'fixedBox': True
    #     })
    #     return form


admin.site.register(News, NewsAdmin)
