from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .api_views import OrganizationViewSet


router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet,
                basename='organizations')

urlpatterns = [
    path('', include(router.urls)),
]
