
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from catalog.models import Product, ProductCategory


class ProductCategorySitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ProductCategory.objects.published()

    def lastmod(self, obj):
        return obj.date_updated


class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Product.objects.published()

    def lastmod(self, obj):
        return obj.date_updated