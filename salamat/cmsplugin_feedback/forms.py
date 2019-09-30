# coding=utf-8
from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Message


class FeedbackMessageForm(forms.ModelForm):
    # name = forms.CharField(label=_('Имя/Компания'),
    #                        widget=forms.TextInput(attrs={'placeholder': _('Имя/Компания')}))
    # email = forms.CharField(label=_('Ваш e-mail'),
    #                         widget=forms.TextInput(attrs={'placeholder': _('Ваш e-mail')}))
    captcha = CaptchaField(
        label=_('Type the code shown'),
        widget=CaptchaTextInput(attrs={'class': 'captcha-input', 'placeholder': _('Type the code shown')}))

    class Meta:
        model = Message
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'email': forms.EmailInput(attrs={'placeholder': _('Email')}),
            'text': forms.Textarea(attrs={'rows': 6, 'placeholder': _('Message')}),
        }
        fields = ('name', 'email', 'text', 'captcha',)
