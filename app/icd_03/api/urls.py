from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import Icd_03ViewSet

router = DefaultRouter()
router.register(r'icd_03', Icd_03ViewSet, basename='icd_03')

urlpatterns = [
    path('', include(router.urls)),
]
