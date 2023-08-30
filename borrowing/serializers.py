from rest_framework import serializers

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
