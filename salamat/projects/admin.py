
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from filesoup.forms import UploaderFormMixin
from filesoup.mixins import RequestProvidingModelAdminMixin
from baseapp.forms import RedactorWidget
from baseapp.helpers import get_assets
from projects.models import Project
from projects.uploaders import AdminProjectImageUploader


class ProjectAdminForm(UploaderFormMixin, forms.ModelForm):
    images = AdminProjectImageUploader.AdminFormField(label=_('Images'))

    class Meta:
        model = Project
        fields = '__all__'

    @property
    def media(self):
        js = get_assets('lib_js', 'fresco_js')
        css = {'all': get_assets('fresco_css')}

        uploader = self['images'].uploader
        redactor_js_url = uploader.reverse(
            'redactor_js', args=(uploader.namespace, uploader.prefix))
        js.append(redactor_js_url)

        media = forms.Media(js=js, css=css)
        return media + super(ProjectAdminForm, self).media


class ProjectAdmin(RequestProvidingModelAdminMixin, admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'active')

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, obj=None, **kwargs)
        form.base_fields['description'].widget = RedactorWidget(options={
            'fixed': True,
            'fixedBox': True
        })
        return form


admin.site.register(Project, ProjectAdmin)
