from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Borrowing, Book, Customer


class BorrowingModelTests(TestCase):
    def setUp(self):
        self.user = Customer.objects.create(
            email="test@example.com", password="pass1234"
        )
        self.book = Book.objects.create(
            title="Test title",
            author="Test author",
            cover=Book.Cover.HARD,
            inventory=5,
            daily_fee=Decimal("1.00"),
        )

    def test_with_valid_data(self):
        borrowing = Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=date.today(),
            book=self.book,
            user=self.user,
        )

        self.assertEquals(Borrowing.objects.count(), 1)
        self.assertEquals(borrowing.borrow_date, date.today())
        self.assertEquals(borrowing.expected_return_date, date.today())
        self.assertEquals(borrowing.actual_return_date, date.today())
        self.assertEquals(borrowing.book, self.book)
        self.assertEquals(borrowing.user, self.user)

    def test_expected_return_date_lower_than_borrow_date(self):
        with self.assertRaises(ValidationError):
            Borrowing.objects.create(
                borrow_date=date(2022, 1, 1),
                expected_return_date=date(2021, 1, 1),
                book=self.book,
                user=self.user,
            )

    def test_actual_return_date_lower_than_borrow_date(self):
        with self.assertRaises(ValidationError):
            Borrowing.objects.create(
                borrow_date=date(2022, 1, 1),
                expected_return_date=date(2022, 1, 1),
                actual_return_date=date(2021, 1, 1),
                book=self.book,
                user=self.user,
            )

    def test_actual_return_date_can_be_null(self):
        Borrowing.objects.create(
            borrow_date=date.today(),
            expected_return_date=date.today(),
            actual_return_date=None,
            book=self.book,
            user=self.user,
        )
