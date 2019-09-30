from django.conf.urls import url
from django.conf.urls import include

from projects.uploaders import AdminProjectImageUploader
from projects.views import ProjectDetailView


urlpatterns = [
    url(r'^admin-project-image-uploader/',
        include(AdminProjectImageUploader.urls)),

    url(r'^(?P<pk>[-\d]+)-(?P<slug>[-\w]+)/$',
        ProjectDetailView.as_view(), name="project_detail"),
]
