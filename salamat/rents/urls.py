from django.conf.urls import url
from django.conf.urls import include

from rents.uploaders import AdminRentsImageUploader
from rents.views import (RentListView, RentDetailView)

from . import views

# app_name = 'rents'
urlpatterns = [
    url(r'^$', RentListView.as_view(), name='rent_list'),
    url(r'^(?P<pk>[\d]+)/$',
        RentDetailView.as_view(), name="rent_detail"),

    url(r'^admin-rents-image-uploader/',
        include(AdminRentsImageUploader.urls)),
]