from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.api.api_views import CustomPageNumberPagination, OR_SEPARATOR
from .serializers import Icd_10Serializer
from ..models import Icd_10


class Icd_10ViewSet(ModelViewSet):
    serializer_class = Icd_10Serializer

    def get_queryset(self):
        queryset = Icd_10.objects.all()

        search_parameters = self.request.query_params.get('code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('diagnosis', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(diagnosis=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('parent', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(parent=param)
            queryset = queryset.filter(query)

        return queryset

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('code', 'diagnosis', 'parent',)
    ordering_fields = ('code', 'diagnosis', 'parent',)
    pagination_class = CustomPageNumberPagination
