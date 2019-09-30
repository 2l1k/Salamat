import django.dispatch
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import mail_managers
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


form_submited = django.dispatch.Signal()

NOTIFY_MANAGERS = True

DEFAULT_NOTIFY_SUBJECT = _('New feedback')
NOTIFY_SUBJECT = DEFAULT_NOTIFY_SUBJECT


def notify_managers(sender, message, request, *args, **kwargs):
    if NOTIFY_MANAGERS:
        s = get_current_site(request)
        mail = EmailMultiAlternatives('%s_%s' % (s.domain, NOTIFY_SUBJECT),
                                      render_email(message, request), settings.DEFAULT_FROM_EMAIL, [a[1] for a in settings.MANAGERS])
        # if html_message:
        #     mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=True)

    # mail_managers(
    #     subject=settings.NOTIFY_SUBJECT,
    #     message=render_email(message, request),
    #     fail_silently=True)

form_submited.connect(notify_managers)


def get_admin_url(instance, request):
    meta = instance._meta
    model = hasattr('meta', 'model_name') and \
        meta.model_name or meta.model_name
    url_pattern = 'admin:{app}_{model}_change'.format(
        app=meta.app_label, model=model)
    s = get_current_site(request)
    return 'http://' + s.domain + reverse(url_pattern, args=[instance.pk])


def render_email(message, request):
    t = loader.get_template('cms/plugins/feedback-email.html')
    c = Context({
        'message': message,
        'url': get_admin_url(message, request),
    })
    return t.render(c)
