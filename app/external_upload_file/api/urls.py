from django.conf.urls import url
from .api_views import ExternalUploadFileVew

app_name = "external_upload_file"

urlpatterns = [
    url(r'upload-files/', ExternalUploadFileVew.as_view(), name='external-upload-file'),
]
