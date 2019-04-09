from rest_framework.pagination import PageNumberPagination

class ArticlePageNumberPagination(PageNumberPagination):
    page_size = 10
    offset_query_param = 'page'
    page_size_query_param = 'limit'

