"""
A URL conf for development only.
"""
from django.conf import settings

from django.conf.urls.static import static
from baseapp.urls import urlpatterns

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
