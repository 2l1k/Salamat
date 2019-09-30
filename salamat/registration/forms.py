# coding=utf-8

from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, Button, Hidden

from userena.forms import (AuthenticationForm as UserenaAuthenticationForm,
                           SignupForm as BaseSignupForm, SignupFormOnlyEmail)
from registration.utils import gen_username


class AuthenticationForm(UserenaAuthenticationForm):
    """docstring for AuthenticationForm"""

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        # Dismiss default trans string.
        self.fields['identification'].label = 'Email'

        # Set remember enabled and change trans string.
        self.fields['remember_me'].label = _(u'Remember me')
        self.fields['remember_me'].initial = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'signin-form'
        self.helper.error_text_inline = True
        self.helper.include_media = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('identification', placeholder=u'E-mail',
                  template='fields/field.html'),
            Field('password', placeholder=u'Пароль',
                  template='fields/field.html'),

        )


class SignupForm(SignupFormOnlyEmail):
    company_name = forms.CharField(label=_(u'Название компании'), max_length=200)
    contract_number = forms.CharField(label=_(u'Номер договора с Саламат'), max_length=200)
    email = forms.EmailField(label=_(u'E-mail'))
    phone = forms.CharField(label=_(u'Номер телефона'), max_length=30)

    def save(self):
        self.cleaned_data['username'] = gen_username()
        user = BaseSignupForm.save(self)
        profile = user.profile
        profile.company_name = self.cleaned_data['company_name']
        profile.contract_number = self.cleaned_data['contract_number']
        profile.phone = self.cleaned_data['phone']
        profile.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'signup-form'
        self.helper.error_text_inline = True
        self.helper.include_media = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('company_name', placeholder=u'Название компании',
                  template='fields/field.html'),
            Field('contract_number', placeholder=u'Номер договора с Саламат',
                  template='fields/field.html'),
            Field('email', placeholder=u'E-mail',
                  template='fields/field.html'),
            Field('phone', placeholder=u'Номер телефона',
                  template='fields/field.html'),
            Field('password1', placeholder=u'Пароль',
                  template='fields/field.html'),
            Field('password2', placeholder=u'Подтверждение пароля',
                  template='fields/field.html'),

        )
