
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from baseapp.forms import RedactorWidget
from baseapp.helpers import get_assets

from brands.models import Brand


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'position')

admin.site.register(Brand, BrandAdmin)
