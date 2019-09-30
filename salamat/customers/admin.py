# coding=utf-8

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from filesoup.forms import UploaderFormMixin
from filesoup.mixins import RequestProvidingModelAdminMixin
from baseapp.forms import RedactorWidget
from baseapp.helpers import get_assets
from customers.models import Customer, Review, ClickHistory


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'company_name')
    actions = ('activate_customer',)
    list_filter = ('privacy',)
    search_fields = ('user__email', 'company_name')

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(CustomerAdmin, self).get_form(request, obj=None, **kwargs)
    #     form.base_fields['description'].widget = RedactorWidget(options={
    #         'fixed': True,
    #         'fixedBox': True
    #     })
    #     return form

    def activate_customer(self, request, queryset):
        for c in queryset:
            c.privacy = 'open'
            c.save(privacy=['active'])
    activate_customer.short_description = u'Активировать клинета'

    def get_actions(self, request):
        actions = super(CustomerAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'date_added', 'active')
    list_filter = ('active', )
    actions = ('activate_review',)

    def activate_review(self, request, queryset):
        for review in queryset:
            review.active = True
            review.save(update_fields=['active'])
    activate_review.short_description = u'Активировать отзывы'

admin.site.unregister(Customer)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ClickHistory)

