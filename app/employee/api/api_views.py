from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from app.api.api_views import OR_SEPARATOR, CustomPageNumberPagination
from .serializers import EmployeeSerializer
from ..models import Employee


class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('user__username', 'surname', 'first_name',)
    ordering_fields = ('user__username', 'surname', 'first_name',)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Employee.objects.select_related(
            'position', 'role', 'organization')

        search_parameters = self.request.query_params.get(
            'user__username', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(user__username=param)
            queryset = queryset.filter(query)

        queryset = queryset.order_by('id')

        return queryset

    def _get_filtered_queryset(self, request, queryset):
        search_parameters = self.request.query_params.get('surname', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(surname=param)
            queryset = queryset.filter(query)

        search_parameters = self.request.query_params.get('first_name', None)
        if search_parameters is not None:
            query = Q()
            for param in search_parameters.split(OR_SEPARATOR):
                query |= Q(first_name=param)
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


class AddEmployeeView(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if User.objects.filter(username=request.data.get('username')):
                return Response({'exists': request.data.get('username')})
            else:
                user = User.objects.create_user(username=request.data.get(
                    'username'), password=request.data.get('password'))
                organization = Organization.objects.get_or_create(
                    name=request.data.get('organization'))[0]
                position = Position.objects.get_or_create(
                    position=request.data.get('position'))[0]
                role = Role.objects.get_or_create(
                    role=request.data.get('role'))[0]
                Employee.objects.create(
                    user=user,
                    surname=request.data.get('surname'),
                    first_name=request.data.get('first_name'),
                    patronymic=request.data.get('patronymic'),
                    organization=organization,
                    position=position,
                    role=role
                )
                return Response(status=status.HTTP_201_CREATED)
