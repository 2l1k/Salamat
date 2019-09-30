
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from baseapp.forms import RedactorWidget
from baseapp.helpers import get_assets

from sliders.models import Slider


class SliderAdminForm(forms.ModelForm):

    class Meta:
        model = Slider
        fields = '__all__'

    @property
    def media(self):
        js = get_assets('lib_js', 'fresco_js')
        css = {'all': get_assets('fresco_css')}

        media = forms.Media(js=js, css=css)
        return media + super(SliderAdminForm, self).media


class SliderAdmin(admin.ModelAdmin):
    form = SliderAdminForm
    list_display = ('title', 'position', 'get_place_display', 'active')
    list_filter=('place', 'active')

    def get_form(self, request, obj=None, **kwargs):
        form = super(SliderAdmin, self).get_form(request, obj=None, **kwargs)
        form.base_fields['description'].widget = RedactorWidget(options={
            'fixed': True,
            'fixedBox': True
        })
        return form
admin.site.register(Slider, SliderAdmin)
