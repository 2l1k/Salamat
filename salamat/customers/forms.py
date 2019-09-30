# coding=utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, Button, Hidden

from filesoup.mixins import FormWithRequestMixin

from customers.models import Customer, Review


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('company_name', 'phone', 'building', 'floor',
                  'apartment', 'whatsapp', 'company_desc', 'mugshot')


class ReviewForm(FormWithRequestMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'rating', 'message', )

    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
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
        self.instance.customer = self.customer
        if self.request.user.is_authenticated():
            self.instance.creator = self.request.user
        review = super(ReviewForm, self).save(commit)
        return review
