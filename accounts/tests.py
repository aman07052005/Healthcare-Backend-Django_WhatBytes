from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class AuthTests(APITestCase):
    def test_register_and_login(self):
        response = self.client.post("/api/auth/register/", {
            "name": "Test User",
            "email": "test@example.com",
            "password": "StrongPassword123!"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/api/auth/login/", {
            "email": "test@example.com",
            "password": "StrongPassword123!"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
