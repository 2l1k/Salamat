
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from baseapp.forms import RedactorWidget
from baseapp.helpers import get_assets

from notifications.models import Notification


class NotificationAdminForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields = '__all__'

    @property
    def media(self):
        js = get_assets('lib_js', 'fresco_js')
        css = {'all': get_assets('fresco_css')}

        media = forms.Media(js=js, css=css)
        return media + super(NotificationAdminForm, self).media


class NotificationAdmin(admin.ModelAdmin):
    form = NotificationAdminForm
    list_display = ('title', 'active', 'position')

    def get_form(self, request, obj=None, **kwargs):
        form = super(NotificationAdmin, self).get_form(request, obj=None, **kwargs)
        form.base_fields['description'].widget = RedactorWidget(options={
            'fixed': True,
            'fixedBox': True
        })
        return form
admin.site.register(Notification, NotificationAdmin)
