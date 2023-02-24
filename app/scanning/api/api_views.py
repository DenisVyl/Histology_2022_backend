from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.api.api_views import CustomPageNumberPagination

from .serializers import ScanningSerializer
from ..models import Scanning


class ScanningViewSet(ModelViewSet):
    serializer_class = ScanningSerializer

    def get_queryset(self):
        queryset = Scanning.objects.all()

        search_parameters = self.request.query_params.get('value', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(value=param)
            queryset = queryset.filter(query)

        return queryset

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('value')
    ordering_fields = ('value')
    pagination_class = CustomPageNumberPagination
