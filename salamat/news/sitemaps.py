
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from news.models import News


class NewsSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return News.objects.published()

    def lastmod(self, obj):
        return obj.date_updated
