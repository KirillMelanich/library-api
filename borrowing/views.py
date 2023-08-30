from django.db import models, transaction
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from book.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.select_related()
    serializer_class = BorrowingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = BorrowingPagination

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        is_active = self.request.query_params.get("is_active")
        if is_active == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)

        user_id = self.request.query_params.get("user_id")
        if str(user_id).isdigit() and self.request.user.is_staff:
            queryset = queryset.filter(user_id=int(user_id))

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        elif self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        book_id = int(self.request.data.get("book"))
        with transaction.atomic():
            Book.objects.filter(id=book_id).update(
                inventory=models.F("inventory") - 1
            )
            serializer.save(user=self.request.user)
