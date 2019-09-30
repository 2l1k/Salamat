# coding: utf-8

from django.views.generic import TemplateView
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


from baseapp.forms import MessageForm
from baseapp.helpers import get_site_url


def send_email(params, context, to):

    context['STATIC_URL'] = settings.STATIC_URL
    context['SITE_URL'] = get_site_url()
    context = Context(context)
    text = get_template(params['template_text'])
    text_content = text.render(context)
    msg = EmailMultiAlternatives(
        params['subject'], text_content, settings.DEFAULT_FROM_EMAIL, to)
    if 'template_html' in params:
        html = get_template(params['template_html'])
        html_content = html.render(context)
        msg.attach_alternative(html_content, "text/html")
    msg.send()


class ContactsVew(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        ctx = super(ContactsVew, self).get_context_data(**kwargs)
        return ctx

    def post(self, request, *args, **kwargs):
        #  if request.is_ajax():
        self.form = MessageForm(request.POST)
        if self.form.is_valid():
            subject = self.form.cleaned_data.get('subject')
            if not subject:
                subject = u'Новое письмо от %s!' % self.form.cleaned_data['name']
            params = {
                'subject': subject,
                'template_text': 'includes/message.txt',
            }
            try:
                send_email(params, self.form.cleaned_data, [a[1] for a in settings.MANAGERS])
            except:
                messages.error(request, _(u'Письмо не отправлено'))
            else:
                messages.success(request, _(u'Спасибо! Ваше сообщение успешно отправлено'))
        else:
            messages.error(request, _(u'Письмо не отправлено'))

        #return HttpResponse(u'Сообщение отправленно! \n Мы обязательно ответим вам')
        #return HttpResponseRedirect(reverse('contacts'))
        link = request.POST.get('redirect_url', '/contacts/')
        return HttpResponseRedirect(link)

class MobileContactsVew(ContactsVew):
    template_name = 'mobile/contacts.html'