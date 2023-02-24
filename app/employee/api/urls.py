from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import EmployeeViewSet, AddEmployeeView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employees')

urlpatterns = [
    path('', include(router.urls)),
    url(r'add_employee/', AddEmployeeView.as_view(), name='add-employee'),
]
