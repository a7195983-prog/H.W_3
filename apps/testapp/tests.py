from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class JwtEndpointsTests(APITestCase):
    def setUp(self):
        self.password = 'strong-password-123'
        self.user = get_user_model().objects.create_user(
            email='student@example.com',
            username='student',
            password=self.password,
            role='USER',
        )

    def login(self):
        response = self.client.post('/api/token/', {
            'email': self.user.email,
            'password': self.password,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data

    def test_login_includes_user_and_access_lifetime_is_15_minutes(self):
        data = self.login()

        self.assertEqual(data['user'], {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'role': self.user.role,
        })
        access_token = AccessToken(data['access'])
        self.assertEqual(access_token['exp'] - access_token['iat'], 15 * 60)

    def test_stats_and_logout_blacklist_refresh_token(self):
        data = self.login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {data['access']}")

        stats_response = self.client.get('/api/profile/stats/')
        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)
        self.assertEqual(stats_response.data['email'], self.user.email)
        self.assertEqual(stats_response.data['role'], self.user.role)
        self.assertFalse(stats_response.data['is_staff'])

        logout_response = self.client.post('/api/logout/', {'refresh': data['refresh']}, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)

        refresh_response = self.client.post('/api/token/refresh/', {'refresh': data['refresh']}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

# Create your tests here.
