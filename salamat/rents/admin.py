
from django.contrib import admin
from rents.models import Rent
from baseapp.forms import RedactorWidget



from django import forms
from django.forms import Media
from django.utils.translation import ugettext_lazy as _

from filesoup.forms import UploaderFormMixin
from filesoup.mixins import RequestProvidingModelAdminMixin

from baseapp.helpers import get_assets
from rents.uploaders import AdminRentsImageUploader


class RentAdminForm(UploaderFormMixin, forms.ModelForm):
    images = AdminRentsImageUploader.AdminFormField(label=_('Images'))

    class Meta:
        model = Rent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RentAdminForm, self).__init__(*args, **kwargs)
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
        return Media(js=js2, css={'all': css2}) + super(RentAdminForm, self).media


class RentAdmin(RequestProvidingModelAdminMixin, admin.ModelAdmin):
    form = RentAdminForm
    list_display = ('category','building', 'area', 'active')
    list_filter = ('category','building', 'active')

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(RentAdmin, self).get_form(request, obj=None, **kwargs)
    #     form.base_fields['description'].widget = RedactorWidget(options={
    #         'fixed': True,
    #         'fixedBox': True
    #     })
    #     return form


admin.site.register(Rent, RentAdmin)
