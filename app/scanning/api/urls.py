from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .api_views import ScanningViewSet

router = DefaultRouter()
router.register(r'scanning', ScanningViewSet, basename='scanning')

urlpatterns = [
    path('', include(router.urls))
]
