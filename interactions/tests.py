from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Like

User = get_user_model()


class LikeTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email='first@example.com',
            password='StrongPass2026!',
        )
        self.user2 = User.objects.create_user(
            email='second@example.com',
            password='StrongPass2026!',
        )
        self.client.force_authenticate(user=self.user1)

    def test_user_can_like_another_user(self):
        response = self.client.post(
            '/api/interactions/likes/',
            {
                'to_user': self.user2.id,
                'action': 'like',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Like.objects.filter(
                from_user=self.user1,
                to_user=self.user2,
                action='like',
            ).exists()
        )

    def test_user_cannot_like_themselves(self):
        response = self.client.post(
            '/api/interactions/likes/',
            {
                'to_user': self.user1.id,
                'action': 'like',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)