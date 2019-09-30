
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from projects.models import Project


class ProjectSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Project.objects.published()

    def lastmod(self, obj):
        return obj.date_updated
