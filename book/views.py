from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

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


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = BookPagination

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        elif self.action == "retrieve":
            return BookDetailSerializer

        return BookSerializer
