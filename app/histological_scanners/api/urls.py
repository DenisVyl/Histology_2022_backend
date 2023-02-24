from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import HistologicalScannersViewSet

router = DefaultRouter()
router.register(r'histological_scanners',
                HistologicalScannersViewSet, basename='histological_scanners')

urlpatterns = [
    path('', include(router.urls))
]
