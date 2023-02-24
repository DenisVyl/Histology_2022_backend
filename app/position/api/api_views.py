from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import PositionSerializer
from ..models import Position

from app.api.api_views import OR_SEPARATOR, CustomPageNumberPagination


class PositionViewSet(ModelViewSet):
    serializer_class = PositionSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('position',)
    ordering_fields = ('position',)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Position.objects.all().order_by('id')

        search_parameters = self.request.query_params.get('position', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(position=param)
            queryset = queryset.filter(query)

        return queryset
