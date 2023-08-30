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
            raise ValidationError(f"Book is out of stock (book_id={book.id})")

        return data

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "book",
        )
