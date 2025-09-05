from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class UsersTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")  # match urls.py name
        self.login_url = reverse("login")        # match urls.py name
        self.user_data = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test User"
        }
        self.user = User.objects.create_user(
            email="existing@example.com",
            password="testpass123",
            name="Existing User"
        )

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_login_user(self):
        response = self.client.post(self.login_url, {
            "email": "existing@example.com",
            "password": "testpass123"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_register_and_login(self):
        # Register
        reg_response = self.client.post(self.register_url, {
            "email": "newuser@example.com",
            "password": "newpass123",
            "name": "New User"
        }, format="json")
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)

        # Login
        login_response = self.client.post(self.login_url, {
            "email": "newuser@example.com",
            "password": "newpass123"
        }, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)
