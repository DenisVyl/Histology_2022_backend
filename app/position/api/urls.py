from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import PositionViewSet

router = DefaultRouter()
router.register(r'positions', PositionViewSet, basename='positions')

urlpatterns = [
    path('', include(router.urls)),
]
