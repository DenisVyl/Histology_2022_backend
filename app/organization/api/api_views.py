from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import OrganizationSerializer
from ..models import Organization
from app.api.api_views import OR_SEPARATOR, CustomPageNumberPagination


class OrganizationViewSet(ModelViewSet):
    serializer_class = OrganizationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('full_name', 'name', 'code')
    ordering_fields = ('full_name', 'name', 'code')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Organization.objects.all().order_by('id')

        search_parameters = self.request.query_params.get('full_name', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(full_name=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('name', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(name=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(code=param)
            queryset = queryset.filter(query)

        return queryset
