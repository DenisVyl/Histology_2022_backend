from rest_framework import status
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView


from app.api.api_views import CustomPageNumberPagination, OR_SEPARATOR
from app.employee.models import Employee
from .serializers import SlideSerializer, SlideLoadingStateSerializer
from ..models import Slide, SlideLoadingState
from ..lib.rsync_file import rsync_file


class SlideViewSet(ModelViewSet):
    serializer_class = SlideSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('slide_id', 'slide_name', 'series__main_code',
                     'series__series_id', 'Icd_10_code__code', 'additional_code', 'focus')
    ordering_fields = ('slide_id', 'slide_name', 'series__main_code',
                       'series__series_id', 'Icd_10_code__code', 'additional_code', 'focus')
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
            queryset = Slide.objects.all()
        else:
            queryset = Slide.objects.\
                select_related('series__research__organization').\
                filter(series__research__organization=employee.organization)

        queryset = queryset.order_by('slide_id')

        return queryset

    def _get_filtered_queryset(self, request, queryset):
        search_parameters = self.request.query_params.get(
            'series__series_id', None)

        if not search_parameters or not len(search_parameters):
            queryset = Slide.objects.none()
            return queryset

        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(series__series_id=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('slide_id', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(slide_id=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('slide_name', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(slide_name=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'series__main_code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(series__main_code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'Icd_10_code__code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(Icd_10_code__code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'additional_code', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(additional_code=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get(
            'focus', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(focus=param)
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


class SlideLoadingStateViewSet(ListModelMixin, GenericAPIView):
    """Rsync viewset class
    """
    serializer_class = SlideLoadingStateSerializer
    queryset = SlideLoadingState.objects.select_related(
        'slide__series__research__organization').order_by('state')
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('state',)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()

        employee = Employee.objects.filter(
            user=self.request.user).select_related('organization').first()

        if not employee.organization.is_admin_organization:
            qs = qs.filter(
                slide__series__research__organization=employee.organization)

        return qs

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def _get_filtered_queryset(self, request, queryset):
        state_search_parameters = self.request.query_params.get(
            'state', None)

        if state_search_parameters:
            queryset = queryset.filter(state=state_search_parameters)

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
