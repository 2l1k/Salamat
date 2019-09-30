from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap, index as index_sitemap
from django.contrib import sitemaps
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, RedirectView
from django.contrib import admin

from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap

from customers.sitemaps import CustomerSitemap
from catalog.sitemaps import ProductCategorySitemap, ProductSitemap
from catalog.uploaders import ProductImageUploader
from projects.sitemaps import ProjectSitemap


from baseapp.views import ContactsVew
# from baseapp.adminsite import admin

admin.autodiscover()

urlpatterns = [
    # url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
    url(r'^catalog/product-image-uploader/', include(ProductImageUploader.urls)),

]

urlpatterns += staticfiles_urlpatterns()

# note the django CMS URLs included via i18n_patterns
urlpatterns += i18n_patterns(
    url(r'^', include('customers.urls')),
    # url(r'^search/', include('haystack.urls')),
    url(r'^feedback/', ContactsVew.as_view(), name="feedback"),
    url(r'^c22596d12ab0.html$', TemplateView.as_view(template_name='ya.html')),
    url(r'^rent/', include('rents.urls')),
    url(r'^news/', include('news.urls')),

    url(r'^catalog/', include('catalog.urls')),
    url(r'^objects/', include('projects.urls')),

    url(r'^me/', include('customers.urls_me')),
    url(r'^auth/', include('registration.urls')),
    url(r'^captcha/', include('captcha.urls')),
    # url(r'^feedback/', include('cmsplugin_feedback.urls')),
    url(r'^robots\.txt', TemplateView.as_view(template_name='robots.txt',
                                              content_type='text/plain')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)


sitemaps = {
    'pages': CMSSitemap,
    'categories': ProductCategorySitemap,
    'products': ProductSitemap,
    'shops': CustomerSitemap,
    'projects': ProjectSitemap
}

urlpatterns += [
    url(r'^sitemap.xml$', cache_page(86400)(index_sitemap),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(86400)(sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),]

