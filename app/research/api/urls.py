from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .api_views import ResearchViewSet, ResearchSeriesSlidesViewSet, UploadView, SandboxCheckView

router = DefaultRouter()
router.register(r'researches', ResearchViewSet, basename='researches')
# router.register(r'researches-series-slides', ResearchSeriesSlidesViewSet,
#                basename='researches-series-slides')

urlpatterns = [
    path('', include(router.urls)),
    url(r'upload/', UploadView.as_view(), name='file-upload'),
    url(r'sandbox_check/', SandboxCheckView.as_view(), name='sandbox-check'),
    url(r'researches-series-slides', ResearchSeriesSlidesViewSet.as_view(),
        name='researches-series-slides')
]
