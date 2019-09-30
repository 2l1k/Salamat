import datetime
from haystack import indexes
from catalog.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    url = indexes.CharField(model_attr='get_absolute_url')
    # date_updated = indexes.DateTimeField(model_attr='date_updated')

    def get_model(self):
        return Product

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().objects.filter(date_updated__lte=datetime.datetime.now())

    def prepare_url(self, obj):
        return obj.get_absolute_url()
