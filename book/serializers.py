from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "inventory", "daily_fee"]


class BookListSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(source="get_cover_display")

    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover"]


class BookDetailSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(source="get_cover_display")

    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "inventory", "daily_fee"]
