from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from book.models import Book
from book.permissions import IsAdminOrReadOnly
from book.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class BookPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(
        summary="List all books",
        description="Get a paginated list of all books",
    ),
    create=extend_schema(summary="Create a new book", description="Create a new book"),
    retrieve=extend_schema(
        summary="Retrieve a book",
        description="Get detailed information about a book",
    ),
    update=extend_schema(summary="Update a book", description="Update a book"),
    partial_update=extend_schema(
        summary="Partially update a book",
        description="Update one or more fields of a book",
    ),
    destroy=extend_schema(summary="Delete a book", description="Delete a book"),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.order_by("title", "author")
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = BookPagination

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        elif self.action == "retrieve":
            return BookDetailSerializer

        return BookSerializer
