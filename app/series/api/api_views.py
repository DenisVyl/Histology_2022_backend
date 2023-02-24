from django.db.models import Q
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from app.employee.models import Employee
from app.api.api_views import OR_SEPARATOR, CustomPageNumberPagination

from ..models import Series
from .serializers import SeriesSerializer, SeriesSlidesSerializer


class SeriesViewSet(ModelViewSet):
    serializer_class = SeriesSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('series_id', 'main_code', 'research__base_code', 'research__research_id',
                     'macroscopic_description', 'microscopic_description', 'Icd_10_code__code', 'histological_diagnosis',)
    ordering_fields = ('series_id', 'main_code', 'research__base_code', 'research__research_id',
                       'macroscopic_description', 'microscopic_description', 'Icd_10_code__code', 'histological_diagnosis',)
    pagination_class = CustomPageNumberPagination

    def get_object(self):
        pk = self.kwargs.get('pk')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        employee = Employee.objects.filter(
            user=self.request.user).select_related('organization').first()

        if employee.organization.is_admin_organization:
            queryset = Series.objects.select_related(
                'research__organization', 'Icd_10_code', 'Icd_03_code').all()
        else:
            queryset = Series.objects.select_related('research__organization').filter(
                research__organization=employee.organization)

        queryset = queryset.order_by('series_id')

        return queryset

    def _get_filtered_queryset(self, request, queryset):
        search_parameters = self.request.query_params.get(
            'research__research_id', None)

        if not search_parameters or not len(search_parameters):
            queryset = Series.objects.none()
            return queryset

        query = Q()
        for param in search_parameters.split(OR_SEPARATOR):
            query |= Q(research__research_id=param)
        queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('series_id', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(series_id=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('main_code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(main_code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'research__base_code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(research__base_code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'macroscopic_description', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(macroscopic_description=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'Icd_10_code__code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(Icd_10_code__code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'histological_diagnosis', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(histological_diagnosis=param)
            queryset = queryset.filter(query)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self._get_filtered_queryset(request, queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class SeriesSlidesViewSet(SeriesViewSet):
    serializer_class = SeriesSlidesSerializer
