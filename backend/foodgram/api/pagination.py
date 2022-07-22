from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    def get_page_size(self, request):
        try:
            return int(request.query_params['limit'])
        except (KeyError, ValueError):
            pass
