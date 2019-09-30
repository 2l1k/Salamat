
from django.contrib.sitemaps import Sitemap

from customers.models import Customer


class CustomerSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return Customer.objects.published()

    def lastmod(self, obj):
        product = obj.user.product_set.first()
        if product:
            return product.date_updated
        return obj.user.date_joined
