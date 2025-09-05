# backend/tasks/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Task


class TasksTests(APITestCase):
    def setUp(self):
        # create test user
        self.user = User.objects.create_user(
            email="test@example.com", name="Test User", password="testpass123"
        )
        # login to get JWT token
        url = reverse("login")  # uses the "name" from urls.py
        r = self.client.post(
            url, {"email": "test@example.com", "password": "testpass123"}
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK, r.content)  # sanity check
        self.token = r.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_task(self):
        url = reverse("task-list")
        data = {"title": "Test Task", "description": "Testing task creation"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tasks(self):
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task(self):
        task = Task.objects.create(title="Old", description="Old desc", owner=self.user)
        url = reverse("task-detail", args=[task.id])
        response = self.client.put(
            url, {"title": "New", "description": "Updated desc"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_task(self):
        task = Task.objects.create(title="Temp", description="Temp desc", owner=self.user)
        url = reverse("task-detail", args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_only_owner_can_delete(self):
        other_user = User.objects.create_user(
            email="other@example.com", name="Other User", password="otherpass123"
        )
        task = Task.objects.create(title="Not Yours", description="...", owner=other_user)
        url = reverse("task-detail", args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
