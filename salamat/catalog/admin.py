# coding=utf-8

from django.contrib import admin
from django import forms
from django.forms import Media
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models import ManyToOneRel
from django.core.urlresolvers import NoReverseMatch

from filesoup.forms import UploaderFormMixin
from filesoup.mixins import RequestProvidingModelAdminMixin
from baseapp.forms import RedactorWidget, TreeNodeChoiceField
from baseapp.helpers import get_assets

from catalog.models import ProductCategory, Product, ProductType, ProductCharacteristic, Review
from catalog.uploaders import AdminProductImageUploader



class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1


class ProductAdminForm(UploaderFormMixin, forms.ModelForm):
    images = AdminProductImageUploader.AdminFormField(label=_('Images'))

    class Meta:
        model = Product
        fields = '__all__'

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
        setup_js_url = uploader.reverse(
            'setup_js', args=(uploader.namespace, uploader.prefix))
        js2.append(setup_js_url)
        return Media(js=js2, css={'all': css2}) + super(ProductAdminForm, self).media


class ProductAdmin(RequestProvidingModelAdminMixin, admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('title', 'category', 'company', 'active')
    search_fields = ('user__email', 'user__profile__company_name')
    inlines = [
        ProductCharacteristicInline,
    ]
    filter_horizontal = ('related_products',)

    def company(self, obj):
        if obj.user:
            return obj.user.profile.company_name
        else:
            ''

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj=None, **kwargs)
        form.base_fields['description'].widget = RedactorWidget(options={
            'fixed': True,
            'fixedBox': True
        })
        return form


class CategoryAdminForm(forms.ModelForm):
    """Form for Category's Admin"""
    parent = TreeNodeChoiceField(
        label=_('parent category').capitalize(),
        required=False, empty_label=_('No parent category'),
        queryset=ProductCategory.objects.all())

    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        rel = ManyToOneRel(ProductCategory, 'id')
        self.fields['parent'].widget = RelatedFieldWidgetWrapper(
            self.fields['parent'].widget, rel, self.admin_site)

    def clean_parent(self):
        """Check if category parent is not selfish"""
        data = self.cleaned_data['parent']
        if data == self.instance:
            raise forms.ValidationError(
                _('A category cannot be parent of itself.'))
        return data

    class Meta:
        """CategoryAdminForm's Meta"""
        model = ProductCategory
        fields = '__all__'


class ProductCategoryAdmin(admin.ModelAdmin):
    # form = CategoryAdminForm
    list_display = ('path', 'position', 'parent', 'active')
    search_fields = ('title', )
    # list_filter = ('parent',)
    #
    # def __init__(self, model, admin_site):
    #     self.form.admin_site = admin_site
    #     super(ProductCategoryAdmin, self).__init__(model, admin_site)
    #
    # def get_tree_path(self, category):
    #     """Return the category's tree path in HTML"""
    #     try:
    #         return '<a href="%s" target="blank">/%s/</a>' % \
    #                (category.get_absolute_url(), category.tree_path)
    #     except NoReverseMatch:
    #         return '/%s/' % category.tree_path
    #
    # get_tree_path.allow_tags = True
    # get_tree_path.short_description = _('tree path')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'date_added', 'active')
    list_filter = ('active', )
    actions = ('activate_review',)

    def activate_review(self, request, queryset):
        for review in queryset:
            review.active = True
            review.save(update_fields=['active'])
    activate_review.short_description = u'Активировать отзывы'

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductType)
admin.site.register(ProductCharacteristic)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)