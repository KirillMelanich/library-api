from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_URL = reverse("user:register")
MANAGE_URL = reverse("user:manage")


class CustomerViewTests(TestCase):
    def test_create_user(self):
        payload = {"email": "test@example.com", "password": "pass1234"}
        response = self.client.post(CREATE_URL, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(
            get_user_model().objects.get().email, payload["email"]
        )

    def test_manage_unauthenticated_user(self):
        response = self.client.get(MANAGE_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_manage_authenticated_user(self):
        user = get_user_model().objects.create_user(
            email="test@example.com", password="pass1234"
        )
        self.client = APIClient()
        self.client.force_authenticate(user)
        response = self.client.get(MANAGE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
