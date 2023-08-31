from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Book
from ..serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
)


class AdminBookViewSetTests(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="Test title 1",
            author="Test author 1",
            cover=Book.Cover.HARD,
            inventory=1,
            daily_fee=Decimal("10.00"),
        )
        self.book2 = Book.objects.create(
            title="Test title 2",
            author="Test author 2",
            cover=Book.Cover.SOFT,
            inventory=2,
            daily_fee=Decimal("20.00"),
        )

        self.user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="pass1234"
        )
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        url = reverse("book:book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

        serializer = BookListSerializer([self.book1, self.book2], many=True)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_retrieve_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = BookDetailSerializer(self.book1)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        url = reverse("book:book-list")
        data = {
            "title": "Test title",
            "author": "Test author",
            "cover": Book.Cover.SOFT,
            "inventory": 3,
            "daily_fee": 3.00,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(title="Test title")
        serializer = BookSerializer(book)
        self.assertEqual(response.data, serializer.data)

    def test_update_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        data = {
            "title": "Updated title",
            "inventory": 0,
        }
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        serializer = BookSerializer(self.book1)
        self.assertEqual(response.data, serializer.data)

    def test_delete_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.filter(pk=self.book1.pk).count(), 0)


class UserBookViewSetTests(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="Test title 1",
            author="Test author 1",
            cover=Book.Cover.HARD,
            inventory=1,
            daily_fee=Decimal("10.00"),
        )
        self.book2 = Book.objects.create(
            title="Test title 2",
            author="Test author 2",
            cover=Book.Cover.SOFT,
            inventory=2,
            daily_fee=Decimal("20.00"),
        )

        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="pass1234"
        )
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        url = reverse("book:book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

        serializer = BookListSerializer([self.book1, self.book2], many=True)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_retrieve_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = BookDetailSerializer(self.book1)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        url = reverse("book:book-list")
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.patch(url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AnonymousBookViewSetTests(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(
            title="Test title 1",
            author="Test author 1",
            cover=Book.Cover.HARD,
            inventory=1,
            daily_fee=Decimal("10.00"),
        )
        self.book2 = Book.objects.create(
            title="Test title 2",
            author="Test author 2",
            cover=Book.Cover.SOFT,
            inventory=2,
            daily_fee=Decimal("20.00"),
        )

    def test_list_books(self):
        url = reverse("book:book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 2)

        serializer = BookListSerializer([self.book1, self.book2], many=True)
        self.assertEqual(response.data.get("results"), serializer.data)

    def test_retrieve_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = BookDetailSerializer(self.book1)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        url = reverse("book:book-list")
        response = self.client.post(url, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.patch(url, {})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book(self):
        url = reverse("book:book-detail", args=[self.book1.pk])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
