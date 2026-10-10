from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegistrationTests(APITestCase):
    def test_register_user(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'email': 'newuser@example.com',
                'password': 'StrongPass2026!',
                'first_name': 'Анна',
                'last_name': 'Иванова',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(email='newuser@example.com').exists()
        )

    def test_register_duplicate_email(self):
        User.objects.create_user(
            email='existing@example.com',
            password='StrongPass2026!',
        )

        response = self.client.post(
            '/api/auth/register/',
            {
                'email': 'existing@example.com',
                'password': 'StrongPass2026!',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)