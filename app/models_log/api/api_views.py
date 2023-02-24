from django.db.models import Q
from models_logging.models import Change
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.api.api_views import CustomPageNumberPagination
from .serializers import ChangeSerializer


class ChangeViewSet(ModelViewSet):
    serializer_class = ChangeSerializer

    def get_queryset(self):
        queryset = Change.objects.all()

        search_parameters = self.request.query_params.get('id', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(id=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('date_created', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(date_created=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('user', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(user=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('object_repr', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(object_repr=param)
            queryset = queryset.filter(query)
        return queryset

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('id', 'date_created', 'user', 'object_repr')
    ordering_fields = ('id', 'date_created', 'user', 'object_repr')
    pagination_class = CustomPageNumberPagination
