
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.conf.urls import url
from views import ContactsVew, MobileContactsVew

@apphook_pool.register
class ContactsApphook(CMSApp):
    name = "Contacts Application"
    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', ContactsVew.as_view()),
        ]


@apphook_pool.register
class MobileContactsApphook(CMSApp):
    name = "Mobile Contacts Application"
    def get_urls(self, page=None, language=None, **kwargs):
        return [
            url(r'^$', MobileContactsVew.as_view()),
        ]