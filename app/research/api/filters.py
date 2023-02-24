from django.db.models import Q
from rest_framework.filters import SearchFilter

OPERATOP_AND = 'and'
OPERATOP_OR = 'or'

OPERATION_EQUAL = 'equal'
OPERATION_NOT = 'not'


class ResearchSeriesSlidesFilter():
    def _proccess_request_filter(self, request_filter):
        filter_name = request_filter.get('columnName')
        filter_list = list(filter(lambda filter: filter.get(
            'name') == filter_name, self.filterset))

        if filter_list:
            filter_dict = filter_list[0]

            return filter_dict

    def _process_single_filter_query(self, filter_dict, request_filter):
        filter_query = Q()

        filter_value = request_filter.get('value')
        fields = filter_dict['fields']
        is_multiple_fields = True if len(fields) > 1 else False

        for field in fields:
            filter_request = {}
            operation = request_filter.get('operation')

            field_by_operation = field if operation == OPERATION_EQUAL else f'{field}__contains'
            filter_request[field_by_operation] = filter_value

            query_by_operation = ~Q(
                **filter_request) if OPERATION_NOT in operation else Q(**filter_request)

            if is_multiple_fields:
                filter_query |= query_by_operation
            else:
                filter_query &= query_by_operation

        return filter_query

    def _process_multiple_filter_query(self, filter_dict, request_filter):
        nested_request_filter = request_filter.get('filters')
        operator = request_filter.get('operator')

        filter_query = self._get_filter_query(
            nested_request_filter, operator=operator)

        return filter_query

    def _get_request_filter_query(self, filter_dict, request_filter):
        if request_filter.get('filters'):
            filter_query = self._process_multiple_filter_query(
                filter_dict, request_filter)
        else:
            filter_query = self._process_single_filter_query(
                filter_dict, request_filter)

        return filter_query

    def _get_filter_query(self, request_filters, operator=OPERATOP_AND):
        filter_query = Q()

        for request_filter in request_filters:
            filter_dict = self._proccess_request_filter(
                request_filter)

            if all((filter_dict, operator == OPERATOP_AND)):
                filter_query &= self._get_request_filter_query(
                    filter_dict, request_filter)

            if all((filter_dict, operator == OPERATOP_OR)):
                filter_query |= self._get_request_filter_query(
                    filter_dict, request_filter)

        return filter_query

    def filter_queryset(self, queryset, request_filters, filterset):
        self.filterset = filterset

        filter_query = self._get_filter_query(request_filters)
        queryset = queryset.filter(filter_query).distinct()

        return queryset


class CustomSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.data.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')

        return params.split()
