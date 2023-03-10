from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import SeriesViewSet

router = DefaultRouter()
router.register(r'series', SeriesViewSet, basename='series')

urlpatterns = [
    path('', include(router.urls))
]
