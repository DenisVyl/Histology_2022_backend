from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .api_views import ChangeViewSet

router = DefaultRouter()
router.register(r'changes', ChangeViewSet, basename='changes')

urlpatterns = [
    path('', include(router.urls))
]
