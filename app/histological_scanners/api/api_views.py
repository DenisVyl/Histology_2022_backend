from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.api.api_views import OR_SEPARATOR, CustomPageNumberPagination

from .serializers import HistologicalScannersSerializer
from ..models import HistologicalScanners


class HistologicalScannersViewSet(ModelViewSet):
    serializer_class = HistologicalScannersSerializer

    def get_queryset(self):
        queryset = HistologicalScanners.objects.all()

        search_parameters = self.request.query_params.get('full_name', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(full_name=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('organization', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(organization=param)
            queryset = queryset.filter(query)

        return queryset

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('full_name', 'code', 'organization')
    ordering_fields = ('full_name', 'code', 'organization')
    pagination_class = CustomPageNumberPagination
