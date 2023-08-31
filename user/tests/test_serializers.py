from django.contrib.auth import get_user_model
from django.test import TestCase

from user.serializers import CustomerSerializer


class CustomerSerializerTests(TestCase):
    def test_create_user_with_success(self):
        payload = {
            "email": "test@test.com",
            "password": "pass1234",
            "first_name": "Test first name",
            "last_name": "Test last name",
        }

        serializer = CustomerSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(user.first_name, payload["first_name"])
        self.assertEqual(user.last_name, payload["last_name"])
        self.assertFalse(user.is_staff)

    def test_create_user_with_error(self):
        payload = {
            "email": "test@test.com",
            "password": "",
        }
        serializer = CustomerSerializer(data=payload)

        self.assertFalse(serializer.is_valid())

    def test_update_user(self):
        payload = {
            "email": "test_upd@test.com",
            "password": "upd45789",
            "first_name": "Updated first name",
            "last_name": "Updated last name",
        }
        user = get_user_model().objects.create_user(
            email="test@test.com", password="pass1234"
        )
        serializer = CustomerSerializer(user, data=payload)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, payload["email"])
        self.assertTrue(updated_user.check_password(payload["password"]))
        self.assertEqual(updated_user.first_name, payload["first_name"])
        self.assertEqual(updated_user.last_name, payload["last_name"])
        self.assertFalse(updated_user.is_staff)
