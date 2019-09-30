from django.conf.urls import url
from django.conf.urls import include

from news.uploaders import AdminNewsImageUploader
from news.views import (NewsListView, NewsDetailView)


urlpatterns = [
    url(r'^admin-news-image-uploader/',
        include(AdminNewsImageUploader.urls)),

    url(r'^$', NewsListView.as_view(), name='news_list'),
    url(r'^(?P<pk>[\d]+)-(?P<slug>[+\-\w]+)/$',
        NewsDetailView.as_view(), name="news_detail"),
]
