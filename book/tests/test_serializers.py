from decimal import Decimal
from django.test import TestCase

from ..models import Book
from ..serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class BookSerializerTests(TestCase):
    def test_book_serializer(self):
        payload = {
            "title": "Test title",
            "author": "Test author",
            "cover": int(Book.Cover.HARD),
            "inventory": 10,
            "daily_fee": "5.25",
        }

        serializer = BookSerializer(data=payload)

        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.data, payload)


class BookListSerializerTests(TestCase):
    def test_book_list_serializer(self):
        payload = {
            "title": "Test title",
            "author": "Test author",
            "cover": int(Book.Cover.HARD),
            "inventory": 1,
            "daily_fee": "1.00",
        }

        book = Book.objects.create(**payload)
        serializer = BookListSerializer(book)

        payload["id"] = book.id
        payload["cover"] = Book.Cover.HARD.label

        self.assertDictEqual(serializer.data, payload)


class BookDetailSerializerTests(TestCase):
    def test_book_detail_serializer(self):
        payload = {
            "title": "Test title",
            "author": "Test author",
            "cover": int(Book.Cover.HARD),
            "inventory": 1,
            "daily_fee": "1.00",
        }

        book = Book.objects.create(**payload)
        serializer = BookListSerializer(book)

        payload["id"] = book.id
        payload["cover"] = Book.Cover.HARD.label

        self.assertDictEqual(serializer.data, payload)
