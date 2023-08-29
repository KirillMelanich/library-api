from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from book.models import Book
from book.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class BookPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        elif self.action == "retrieve":
            return BookDetailSerializer

        return BookSerializer
