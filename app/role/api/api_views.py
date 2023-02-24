from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.api.api_views import CustomPageNumberPagination

from .serializers import RoleSerializer
from ..models import Role


class RoleViewSet(ModelViewSet):
    serializer_class = RoleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('role')
    ordering_fields = ('role',)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Role.objects.all().order_by('id')

        search_parameters = self.request.query_params.get('role', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(role=param)
            queryset = queryset.filter(query)

        return queryset
