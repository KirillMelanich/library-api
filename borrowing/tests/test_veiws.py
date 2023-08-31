from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Customer, Book, Borrowing
from ..serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingReturnSerializer,
)


def create_user():
    return Customer.objects.create(
        email="test@example.com", password="pass1234"
    )


def create_book():
    return Book.objects.create(
        title="Test title",
        author="Test author",
        cover=Book.Cover.HARD,
        inventory=5,
        daily_fee=Decimal("5.00"),
    )


def create_borrowing(book, user):
    return Borrowing.objects.create(
        borrow_date="2023-01-01",
        expected_return_date="2023-01-01",
        book=book,
        user=user,
    )


class AdminBorrowingViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = create_user()
        self.book1 = create_book()
        self.borrowing1 = create_borrowing(self.book1, self.user1)

        self.user2 = get_user_model().objects.create_superuser(
            email="admin@example.com", password="pass1234"
        )
        self.client.force_authenticate(self.user2)

    def test_list_borrowings(self):
        url = reverse("borrowing:borrowing-list")
        create_borrowing(self.book1, self.user2)

        borrowing_list = Borrowing.objects.order_by("-borrow_date", "-id")
        serializer = BorrowingSerializer(borrowing_list, many=True)

        self.assertEqual(len(borrowing_list), 2)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_borrowings_for_is_active_eq_true(self):
        url = reverse("borrowing:borrowing-list") + "?is_active=true"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_borrowings_for_is_active_eq_false(self):
        url = reverse("borrowing:borrowing-list") + "?is_active=false"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_list_borrowings_for_user_id_filter(self):
        url = reverse("borrowing:borrowing-list") + "?user_id=1"
        create_borrowing(self.book1, self.user2)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], self.borrowing1.id)

    def test_retrieve_borrowing(self):
        url = reverse(
            "borrowing:borrowing-detail", kwargs={"pk": self.borrowing1.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing1.id)

    def test_create_borrowing(self):
        url = reverse("borrowing:borrowing-list")
        payload = {
            "borrow_date": "2023-01-01",
            "expected_return_date": "2023-01-01",
            "book": 1,
        }

        self.assertEqual(Borrowing.objects.count(), 1)

        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 2)

        borrowing = Borrowing.objects.last()
        serializer = BorrowingCreateSerializer(borrowing)

        self.assertEqual(response.data, serializer.data)

    def test_return_borrowing(self):
        url = reverse(
            "borrowing:borrowing-return", kwargs={"pk": self.borrowing1.id}
        )
        payload = {"actual_return_date": "2023-03-28"}
        response = self.client.post(url, data=payload)

        borrowing = Borrowing.objects.get(id=self.borrowing1.id)
        serializer = BorrowingReturnSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class UserBorrowingViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = create_user()
        self.book1 = create_book()
        self.borrowing1 = create_borrowing(self.book1, self.user1)

        self.user2 = get_user_model().objects.create_user(
            email="test2@example.com", password="pass1234"
        )
        self.book2 = create_book()
        self.borrowing2 = create_borrowing(self.book2, self.user2)

        self.client.force_authenticate(self.user2)

    def test_list_borrowings(self):
        url = reverse("borrowing:borrowing-list")

        borrowing_list = Borrowing.objects.filter(user=self.user2).order_by(
            "-borrow_date", "-id"
        )
        serializer = BorrowingSerializer(borrowing_list, many=True)

        self.assertEqual(len(borrowing_list), 1)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_list_borrowings_for_is_active_eq_true(self):
        url = reverse("borrowing:borrowing-list") + "?is_active=true"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_borrowings_for_is_active_eq_false(self):
        url = reverse("borrowing:borrowing-list") + "?is_active=false"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_retrieve_borrowing(self):
        url = reverse(
            "borrowing:borrowing-detail", kwargs={"pk": self.borrowing2.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.borrowing2.id)

    def test_create_borrowing(self):
        url = reverse("borrowing:borrowing-list")
        payload = {
            "borrow_date": "2023-01-01",
            "expected_return_date": "2023-01-01",
            "book": 1,
        }

        self.assertEqual(Borrowing.objects.filter(user=self.user2).count(), 1)

        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Borrowing.objects.filter(user=self.user2).count(), 2
        )

        borrowing = Borrowing.objects.last()
        serializer = BorrowingCreateSerializer(borrowing)

        self.assertEqual(response.data, serializer.data)

    def test_return_borrowing(self):
        url = reverse(
            "borrowing:borrowing-return", kwargs={"pk": self.borrowing2.id}
        )
        payload = {"actual_return_date": "2023-03-28"}
        response = self.client.post(url, data=payload)

        borrowing = Borrowing.objects.get(id=self.borrowing2.id)
        serializer = BorrowingReturnSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class AnonymousBorrowingViewSetTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.book = create_book()
        self.borrowing = create_borrowing(self.book, self.user)

    def test_list_borrowings(self):
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_borrowing(self):
        url = reverse(
            "borrowing:borrowing-detail", kwargs={"pk": self.borrowing.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_borrowing(self):
        url = reverse("borrowing:borrowing-list")
        payload = {
            "borrow_date": "2023-01-01",
            "expected_return_date": "2023-01-01",
            "book": 1,
        }
        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_borrowing(self):
        url = reverse(
            "borrowing:borrowing-return", kwargs={"pk": self.borrowing.id}
        )
        payload = {"actual_return_date": "2023-03-28"}
        response = self.client.post(url, data=payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
