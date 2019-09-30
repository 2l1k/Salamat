# coding: utf-8

import time
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from userena.signals import activation_complete

from baseapp.views import send_email


@receiver(user_logged_in, dispatch_uid='user_logged_in_handler')
def user_logged_in_handler(sender, user, request, **kwargs):
    messages.info(request, _('Hi, %(username)s!') %
                  dict(username=user.profile.username))


@receiver(user_logged_out, dispatch_uid='user_logged_out_handler')
def user_logged_out_handler(sender, user, request, **kwargs):
    if user:
        messages.info(request, _('Bye, %(username)s.') %
                      dict(username=user.profile.username))
    else:
        messages.info(request, _('You have been signed out.'))


def user_standard_activated(user, **kwargs):
    params = {
        'subject': u'Зарегистрировался новый арендатор %s (%s)!' % (user.profile.company_name, user.profile.contract_number),
        'template_text': 'includes/message.txt',
    }
    data = {
        'name': user.profile.company_name,
        'phone': user.profile.phone,
        'message': u'Зарегистрировался новый арендатор %s (%s) %s!' % (user.profile.company_name, user.profile.contract_number,  user.profile.email),
    }
    try:
        send_email(params, data, [a[1] for a in settings.MANAGERS])
    except:
        time.sleep(1)
        send_email(params, data, [a[1] for a in settings.MANAGERS])

activation_complete.connect(user_standard_activated)