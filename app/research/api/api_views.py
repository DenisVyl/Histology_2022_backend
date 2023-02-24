from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.lib.utils.check_data import check_data
from app.lib.utils.upload_data import upload_data
from app.employee.models import Employee
from app.api.api_views import CustomPageNumberPagination

from ..models import Research
from .paginators import ResearchSeriesSlidesPagination
from .filters import CustomSearchFilter, ResearchSeriesSlidesFilter
from .serializers import ResearchSerializer, ResearchSeriesSerializer


class SandboxCheckView(APIView):
    def post(self, request, *args, **kwargs):
        json_response = check_data(request.data, request.user)

        return Response(json_response)


class UploadView(APIView):
    def post(self, request, *args, **kwargs):
        is_upload_data_successful, errors = upload_data(
            request.data, request.user)

        if not is_upload_data_successful:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


class ResearchViewSet(ModelViewSet):
    serializer_class = ResearchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('base_code', 'year', 'macroscopic_description', 'microscopic_description', 'organization__name',
                     'receipt_date', 'return_date', 'receipt_employee__surname', 'return_employee__surname', 'operator__surname')
    ordering_fields = ('base_code', 'year', 'macroscopic_description', 'microscopic_description', 'organization__name',
                       'receipt_date', 'return_date', 'receipt_employee__surname', 'return_employee__surname', 'operator__surname')
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Research.objects.\
            select_related(
                'organization',
                'operator',
                'receipt_employee',
                'return_employee'
            ).order_by('research_id')

        employee = Employee.objects.filter(
            user=self.request.user).select_related('organization').first()

        if not employee.organization.is_admin_organization:
            queryset = queryset.filter(
                organization=employee.organization)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class ResearchSeriesSlidesViewSet(GenericAPIView):
    serializer_class = ResearchSeriesSerializer
    pagination_class = ResearchSeriesSlidesPagination

    search_fields = (
        'base_code',
        'series__main_code',
        'series__slides__slide_name',
        'series__slides__slide_name',
        'series__Icd_10_code__code', 'series__slides__Icd_10_code__code',
        'series__Icd_03_code__code', 'series__slides__Icd_03_code__code',
        'series__slides__histological_scanner__code',
        'series__histological_diagnosis',
        'macroscopic_description', 'series__macroscopic_description',
        'microscopic_description', 'series__microscopic_description',
        'receipt_employee__surname', 'receipt_employee__first_name',
        'return_employee__surname', 'return_employee__first_name',
        'operator__first_name', 'operator__surname',
    )

    filterset = (
        {
            'name': 'base_code',
            'fields': ('base_code',),
        },
        {
            'name': 'main_code',
            'fields': ('series__main_code',),
        },
        {
            'name': 'slide_name',
            'fields': ('series__slides__slide_name',),
        },
        {
            'name': 'slide_name',
            'fields': ('series__slides__slide_name',),
        },
        {
            'name': 'slides_per_series',
            'fields': ('series__number_of_slides',),
        },
        {
            'name': 'slides_per_research',
            'fields': (),
        },
        {
            'name': 'year',
            'fields': ('year',),
        },
        {
            'name': 'Icd_10_code',
            'fields': ('series__Icd_10_code__code', 'series__slides__Icd_10_code__code',),
        },
        {
            'name': 'Icd_03_code',
            'fields': ('series__Icd_03_code__code', 'series__slides__Icd_03_code__code',),
        },
        {
            'name': 'histological_scanner',
            'fields': ('series__slides__histological_scanner__code',),
        },
        {
            'name': 'scanning',
            'fields': ('series__slides__scanning__value',),
        },
        {
            'name': 'focus',
            'fields': ('series__slides__focus',),
        },
        {
            'name': 'histological_diagnosis',
            'fields': ('series__histological_diagnosis',),
        },
        {
            'name': 'additional_code',
            'fields': ('series__slides__additional_code',),
        },
        {
            'name': 'macroscopic_description',
            'fields': ('macroscopic_description', 'series__macroscopic_description'),
        },
        {
            'name': 'microscopic_description',
            'fields': ('microscopic_description', 'series__microscopic_description'),
        },
        {
            'name': 'organization',
            'fields': ('organization__code',),
        },
        {
            'name': 'receipt_employee',
            'fields': ('receipt_employee__surname', 'receipt_employee__first_name', ),
        },
        {
            'name': 'receipt_date',
            'fields': ('receipt_date',),
        },
        {
            'name': 'return_employee',
            'fields': ('return_employee__surname', 'return_employee__first_name', ),
        },
        {
            'name': 'return_date',
            'fields': ('return_date',),
        },
        {
            'name': 'operator',
            'fields': ('operator__first_name', 'operator__surname'),
        },
    )

    def get_queryset(self):
        queryset = Research.objects.\
            select_related(
                'organization',
                'operator',
                'receipt_employee',
                'return_employee'
            ).prefetch_related(
                'series',
                'series__Icd_10_code',
                'series__Icd_03_code',
                'series__slides',
                'series__slides__Icd_10_code',
                'series__slides__Icd_03_code',
                'series__slides__scanning',
                'series__slides__histological_scanner'
            ).order_by('research_id')

        employee = Employee.objects.filter(
            user=self.request.user).select_related('organization').first()

        if not employee.organization.is_admin_organization:
            queryset = queryset.filter(
                organization=employee.organization)

        return queryset

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        request_filters = request.data.get('filters')
        request_search = request.data.get('search')

        # Custom filtering
        if request_filters:
            queryset = ResearchSeriesSlidesFilter(
            ).filter_queryset(queryset, request_filters, self.filterset)

        # Custom searching
        if request_search:
            queryset = CustomSearchFilter().filter_queryset(
                self.request, queryset, self)

        # Custom pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
