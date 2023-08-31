from decimal import Decimal

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from ..models import Book, Customer, Borrowing
from ..serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


def create_user():
    return Customer.objects.create(email="test@example.com", password="pass1234")


def create_book():
    return Book.objects.create(
        title="Test title",
        author="Test author",
        cover=Book.Cover.HARD,
        inventory=1,
        daily_fee=Decimal("1.00"),
    )


def create_borrowing(book, user):
    return Borrowing.objects.create(
        borrow_date="2023-01-01",
        expected_return_date="2023-01-01",
        book=book,
        user=user,
    )


class BorrowingSerializerTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.book = create_book()
        self.borrowing = create_borrowing(self.book, self.user)

    def test_borrowing_serializer(self):
        self.maxDiff = None
        payload = {
            "id": 1,
            "borrow_date": "2023-01-01",
            "expected_return_date": "2023-01-01",
            "actual_return_date": None,
            "book": {
                "id": 1,
                "title": "Test title",
                "author": "Test author",
                "cover": "Hard",
                "inventory": 1,
                "daily_fee": "1.00",
            },
            "user": {
                "id": 1,
                "email": "test@example.com",
                "first_name": "",
                "last_name": "",
                "is_staff": False,
            },
        }

        serializer = BorrowingSerializer(self.borrowing)

        self.assertDictEqual(serializer.data, payload)


class BorrowingCreateSerializerTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.book = create_book()

    def test_borrowing_create_serializer_valid(self):
        payload = {
            "borrow_date": "2023-01-01",
            "expected_return_date": "2023-01-01",
            "book": 1,
        }
        serializer = BorrowingCreateSerializer(data=payload)

        self.assertTrue(serializer.is_valid())

        prev_inventory = self.book.inventory
        serializer.save(user=self.user)
        self.book.refresh_from_db()

        self.assertEqual(self.book.inventory, prev_inventory - 1)

    def test_borrowing_create_serializer_with_invalid_expected_return_date(
        self,
    ):
        payload = {
            "borrow_date": "2023-01-01",
            "expected_return_date": "2021-01-01",
            "book": 1,
        }
        serializer = BorrowingCreateSerializer(data=payload)

        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError) as e:
            serializer.save(user=self.user)
        self.assertIn(
            "Expected return date should be greater or equal then borrow date",
            e.exception.args[0],
        )

    def test_borrowing_create_serializer_with_book_out_of_stock(self):
        payload = {
            "borrow_date": "2023-01-01",
            "expected_return_date": "2023-01-01",
            "book": 1,
        }
        self.book.inventory = 0
        self.book.save()

        serializer = BorrowingCreateSerializer(data=payload)

        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError) as e:
            serializer.save(user=self.user)

        self.assertIn("The book is out of stock", e.exception.args[0])


class BorrowingReturnSerializerTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.book = create_book()
        self.borrowing = create_borrowing(self.book, self.user)

    def test_borrowing_return_serializer_valid(self):
        payload = {
            "actual_return_date": "2023-01-01",
        }
        serializer = BorrowingReturnSerializer(self.borrowing, data=payload)

        self.assertTrue(serializer.is_valid())

        prev_inventory = self.book.inventory
        serializer.save()
        self.book.refresh_from_db()

        self.assertEqual(self.book.inventory, prev_inventory + 1)

    def test_borrowing_return_serializer_with_invalid_actual_return_date(
        self,
    ):
        payload = {
            "actual_return_date": "2021-01-01",
        }
        serializer = BorrowingReturnSerializer(self.borrowing, data=payload)

        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError) as e:
            serializer.save()

        self.assertIn(
            "Actual return date should be greater or equal then borrow date",
            e.exception.args[0],
        )

    def test_borrowing_return_serializer_with_attempt_to_return_book_twice(
        self,
    ):
        payload = {
            "actual_return_date": "2023-01-01",
        }
        serializer = BorrowingReturnSerializer(self.borrowing, data=payload)

        self.assertTrue(serializer.is_valid())
        serializer.save()

        serializer = BorrowingReturnSerializer(self.borrowing, data=payload)

        self.assertTrue(serializer.is_valid())
        with self.assertRaises(ValidationError) as e:
            serializer.save()

        self.assertIn(
            "The book has already been returned by user",
            e.exception.args[0],
        )
