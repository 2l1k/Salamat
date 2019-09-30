# coding=utf-8

from django import forms

from django.forms import ModelChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, Button, Hidden


from filesoup.forms import UploaderFormMixin
from filesoup.mixins import FormWithRequestMixin

from catalog.models import Product, ProductCharacteristic, ProductCategory, ProductType, Review
from catalog.uploaders import ProductImageUploader


class MyModelChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return '%s' % obj


class SearchForm(forms.Form):
    categories = ModelChoiceField(queryset=ProductCategory.objects.published(), required=False)
    search = forms.CharField()


class ProductBaseForm(forms.ModelForm):
    # category = MyModelChoiceField(queryset=ProductCategory.objects.published().filter(childs__isnull=True),
    #                               empty_label=u'Категория')
    category = forms.TextInput()

    product_type = forms.ModelChoiceField(queryset=ProductType.objects.published(), empty_label=u'Тип')

    class Meta:
        model = Product
        exclude = ('user', 'active')
        widgets = {
            'category': forms.TextInput()
        }


class ProductInfoForm(UploaderFormMixin, ProductBaseForm):
    images = ProductImageUploader.FormField(label=u'Фото')

    def __init__(self, *args, **kwargs):

        super(ProductInfoForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'product-form'
        self.helper.error_text_inline = True
        self.helper.include_media = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(Div(
                Div(
                    Div(
                        Field('title', placeholder=u'Наименование товара',
                              template='fields/field.html'),
                        css_class='col-md-12'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('category', placeholder=u'Категория',
                              template='fields/cat_field.html', css_class='input_cat_btn', readonly=True),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('price', placeholder=u'Цена',
                              template='fields/field.html'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(css_class='col-md-6'),
                    Div(
                        HTML('<label class="checkbox">'),
                        Field('price_from', type='checkbox', hidden='True',
                              template='fields/field.html'),
                        HTML('<span></span>%s</label>' % u'Установить цену от'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                    Div(
                        Field('product_type', placeholder=u'Тип',
                              template='fields/field.html'),
                        css_class='col-md-6'
                    ),
                    Div(
                        Field('quantity', placeholder=u'Количество',
                              template='fields/field.html'),
                        css_class='col-md-6'
                    ),
                    css_class='row'
                ),
                Div(
                Div(
                    Field('description', placeholder=u'Описание товара', rows='4',
                          template='fields/field.html'),
                    css_class='col-xs-12'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('images'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('stock', template='fields/field.html'),
                    Field('brand', placeholder=u'Бренд', template='fields/field.html'),
                    Field('collection', placeholder=u'Коллекция', template='fields/field.html'),
                    Field('color', placeholder=u'Цвет', template='fields/field.html'),
                    css_class='col-md-6'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    HTML('<button class="btn publication"><span>%s'
                         '</span></button>' % u'Опубликовать товар/услугу'),
                    css_class='col-md-6'
                ),
                css_class='row'
            ),
            css_class='form product-info',
        ))


class ProductForm(ProductInfoForm):

    def save(self, commit=True):
        self.cleaned_data['user'] = self.request.user

        product = super(ProductForm, self).save(commit)
        product.user = self.request.user
        product.save()
        return product


class ProductUpdateForm(ProductInfoForm):
    class Meta:
        model = Product
        exclude = ('user', 'active', 'discount_percent', 'discount')
        widgets = {
            'category': forms.TextInput()
        }


class ProductSeoUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('seo_title', 'seo_keywords', 'seo_description')


class ProductDiscountUpdateForm(forms.ModelForm):
    discount_start_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                          input_formats=('%Y-%m-%d',),
                                          required=False)
    discount_end_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'),
                                        input_formats=('%Y-%m-%d',),
                                        required=False)
    class Meta:
        model = Product
        fields = ('discount', 'discount_percent', 'discount_start_date', 'discount_end_date')


class ProductCharacteristicForm(forms.ModelForm):
    images = ProductImageUploader.FormField(label=u'Фото')

    class Meta:
        model = ProductCharacteristic
        fields = ('title', 'characteristic_desc')

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        super(ProductCharacteristicForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'product-form'

        # self.helper.error_text_inline = False
        self.helper.include_media = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div(
                    HTML('<button class="add_specification"><span>'
                         '</span></button>'),
                    Field('title', placeholder=u'Название характеристики',
                          template='fields/field.html'),
                    css_class='col-xs-12'
                ),
                css_class='row'
            ),
            Div(
                Div(
                    Field('characteristic_desc', placeholder=u'Описание',
                          template='fields/field.html'),
                    css_class='col-xs-12'
                ),
                css_class='row'
            ),
        )

    def save(self, commit=True):
        self.instance.product = self.product
        productchar = super(ProductCharacteristicForm, self).save(commit)
        return productchar


class ReviewForm(FormWithRequestMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'rating', 'message', )

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'review-form'
        # self.helper.error_text_inline = False
        self.helper.include_media = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field('title', placeholder=u'Ваше имя', template='fields/field.html'),
                Div(
                    HTML('%s' % u'Пожалуйста, поставьте свою оценку'),
                    Div(
                        Field('rating', type='radio', value='5', checked='checked', hidden=True, template='fields/field.html'),
                        HTML('<label hidden></label><input type="radio" '
                             'id="rating-1" name="rating" value="1" /><label for="rating-1"></label>'
                             '<input type="radio" id="rating-2" name="rating" value="2" />'
                             '<label for="rating-2"></label><'
                             'input type="radio" id="rating-3" name="rating" value="3" />'
                             '<label for="rating-3"></label><input type="radio" id="rating-4" name="rating"'
                             'value="4" /><label for="rating-4"></label><input type="radio" id="rating-5" '
                             'name="rating" value="5" /><label for="rating-5"></label>'),
                        css_class='stars'),
                    css_class='rating'
                ),
                Field('message', placeholder=u'Ваш отзыв', template='fields/field.html'),
                css_class='form',
            ),
        )

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 & rating > 5:
            raise forms.ValidationError(u'Укажите rating')
        return rating

    def save(self, commit=True):
        self.instance.product = self.product
        if self.request.user.is_authenticated():
            self.instance.user = self.request.user
        review = super(ReviewForm, self).save(commit)
        return review
