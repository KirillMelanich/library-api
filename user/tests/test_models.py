from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomerModelTests(TestCase):
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="pass1234",
            first_name="Admin first name",
            last_name="Admin last name",
        )

        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.check_password("pass1234"))
        self.assertEqual(user.first_name, "Admin first name")
        self.assertEqual(user.last_name, "Admin last name")
        self.assertTrue(user.is_staff)

    def test_create_user(self):
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="pass1234",
            first_name="Test first name",
            last_name="Test last name",
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("pass1234"))
        self.assertEqual(user.first_name, "Test first name")
        self.assertEqual(user.last_name, "Test last name")
        self.assertFalse(user.is_staff)
