from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Book


class BookModelTests(TestCase):
    def setUp(self):
        self.origin = Book.objects.create(
            title="Test title",
            author="Test author",
            cover=Book.Cover.HARD,
            inventory=5,
            daily_fee=Decimal("1.23"),
        )

    def test_book_existence_and_data_validation(self):
        book = Book.objects.get(id=1)

        self.assertEquals(book.title, self.origin.title)
        self.assertEquals(book.author, self.origin.author)
        self.assertEquals(book.cover, Book.Cover.HARD)
        self.assertEquals(book.inventory, self.origin.inventory)
        self.assertEquals(book.daily_fee, self.origin.daily_fee)

    def test_book_inventory_positive_validator(self):
        book = Book.objects.get(id=1)
        book.inventory = -1
        with self.assertRaises(ValidationError):
            book.save()

    def test_book_daily_fee_value_validator(self):
        book = Book.objects.get(id=1)

        book.daily_fee = (Decimal("1.2345"),)
        with self.assertRaises(ValidationError):
            book.save()

        book.daily_fee = (Decimal("-1.00"),)
        with self.assertRaises(ValidationError):
            book.save()

    def test_book_string_representation(self):
        book = Book.objects.get(id=1)

        self.assertEquals(str(book), '"Test title" by Test author')
