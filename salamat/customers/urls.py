from django.conf.urls import url

from customers.views import PlanView, ReviewCreateView, show_phone


urlpatterns = [
    url(r'show_phone/$', show_phone, name="show_phone"),
    url(r'^(?P<pk>[-\d]+)/$', ReviewCreateView.as_view(), name='customer_detail'),
    url(r'plan/$', PlanView.as_view(), name="plan"),
]
