from app.api.api_views import CustomPageNumberPagination
from rest_framework.pagination import _positive_int


class ResearchSeriesSlidesPagination(CustomPageNumberPagination):
    def get_page_number(self, request, paginator):
        page_number = request.data.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        return page_number

    def get_page_size(self, request):
        if self.page_size_query_param and \
                request.data.get(self.page_size_query_param):
            try:
                return _positive_int(
                    request.data.get(self.page_size_query_param),
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size
