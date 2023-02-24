from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import SlideViewSet, SlideLoadingStateViewSet

router = DefaultRouter()
router.register(r'slides', SlideViewSet, basename='slides')

urlpatterns = [
    path('', include(router.urls)),
    path('slides-loading-state/', SlideLoadingStateViewSet.as_view()),
]
