import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book.models import Book
from book.serializers import BookDetailSerializer
from borrowing.models import Borrowing
from user.serializers import CustomerSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(many=False, read_only=True)
    user = CustomerSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs=attrs)

        book = get_object_or_404(Book, id=attrs["book"].id)
        if book.inventory == 0:
            raise ValidationError("Book is out of stock")

        return data

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "book",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):
    actual_return_date = serializers.DateField(
        required=True, initial=datetime.date.today
    )

    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        pk = self.context.get("view").kwargs.get("pk")
        borrowing = get_object_or_404(Borrowing, id=pk)

        if borrowing.actual_return_date is not None:
            raise ValidationError("The book has already been returned by user")

        return data

    class Meta:
        model = Borrowing
        fields = ("actual_return_date",)
