from rest_framework import pagination

class JobPaginator(pagination.PageNumberPagination):
    page_size = 8