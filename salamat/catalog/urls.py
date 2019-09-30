from django.conf.urls import url
from django.conf.urls import include

from catalog.uploaders import AdminProductImageUploader, ProductImageUploader
from catalog.views import (ProductDetailView, CategoryDetailView, ProductCreateView, ProductUpdateView,
                           ProductCharacteristicCreateView, ProductCharacteristicDeleteView, ProductSeoUpdateView,
                           ProductDeleteView, ReviewCreateView, ProductSearchView, ProductDiscountUpdateView)


urlpatterns = [
    # url(r'^product-image-uploader/', include(ProductImageUploader.urls)),
    url(r'^admin-product-image-uploader/', include(AdminProductImageUploader.urls)),
    url(r'^search/$', ProductSearchView.as_view(), name='product_search'),
    url(r'^(?P<category_pk>[\d]+)-(?P<category_slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'^(?P<category_pk>[\d]+)-(?P<category_slug>[-\w]+)/(?P<pk>[\d]+)-(?P<slug>[-\w]+)/$',
        ProductDetailView.as_view(), name="product_detail"),
    url(r'add/$', ProductCreateView.as_view(), name="product_create"),
    url(r'^update/(?P<pk>[\d]+)-(?P<slug>[-\w]+)/$', ProductUpdateView.as_view(), name='product_update'),
    url(r'^delete/(?P<pk>[\d]+)-(?P<slug>[-\w]+)/$', ProductDeleteView.as_view(), name='product_delete'),
    url(r'^seo_update/(?P<pk>[\d]+)-(?P<slug>[-\w]+)/$', ProductSeoUpdateView.as_view(), name='product_seo_update'),
    url(r'^discount_update/(?P<pk>[\d]+)-(?P<slug>[-\w]+)/$', ProductDiscountUpdateView.as_view(),
        name='product_discount_update'),
    url(r'^char/add/(?P<product_pk>[\d]+)-(?P<product_slug>[-\w]+)/$',
        ProductCharacteristicCreateView.as_view(), name='product_characteristic_create'),
    url(r'^char/delete/(?P<product_pk>[\d]+)-(?P<product_slug>[-\w]+)/(?P<pk>[\d]+)/$',
        ProductCharacteristicDeleteView.as_view(), name='product_characteristic_delete'),
    url(r'^review/add/(?P<product_pk>[\d]+)-(?P<product_slug>[-\w]+)/$',
        ReviewCreateView.as_view(), name='review_create'),
]
