from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Profile

User = get_user_model()


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='profileuser@example.com',
            password='StrongPass2026!',
        )
        self.client.force_authenticate(user=self.user)

    def test_my_profile_is_available(self):
        response = self.client.get('/api/profiles/me/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Profile.objects.filter(user=self.user).exists()
        )

    def test_update_my_profile(self):
        response = self.client.patch(
            '/api/profiles/me/',
            {
                'city': 'Vienna',
                'bio': 'Люблю путешествия',
                'interests': ['музыка', 'путешествия'],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['city'], 'Vienna')
