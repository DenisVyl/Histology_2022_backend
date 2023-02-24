from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import Icd_10ViewSet

router = DefaultRouter()
router.register(r'icd_10', Icd_10ViewSet, basename='icd_10')

urlpatterns = [
    path('', include(router.urls)),
]
