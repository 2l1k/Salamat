
from django.conf.urls import  url
from customers import views


urlpatterns = [
    url(r'^$', views.me, name='me'),
]
