"""
Tests for users API.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
import json


CREATE_USER_URL = reverse('users:register-user')

def create_user(**params):
    """Register and return a new user."""
    return get_user_model().objects.create_user(**params)

class UsersAPITests(TestCase):
    """Test user API."""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'lazarospk95@gmail.com',
            'password': "mysecuredpassword"
        }

    def test_register_user_success(self):
        """Test registering a user is successful."""

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)

    def test_register_user_without_email(self):
        """Test registering a user is failing."""

        self.payload.pop('email')

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('first_name', res.data)

    def test_register_user_with_weak_password(self):
        """Testing registering a user with weak password is failing"""

        self.payload['password'] = '123'
 
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('email', res.data)

    def test_user_with_email_exists_error(self):
        """Test error is returned if user with same email exists."""

        user = create_user(**self.payload)

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """Testing user login successful."""

        create_user(**self.payload)
        self.payload.pop('first_name')
        self.payload.pop('last_name')

        res = self.client.post(reverse("token"), self.payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)

        return json.loads(json.dumps(res.data))

    def test_user_login_error(self):
        """Testing user login failed."""

        self.payload.pop('first_name')
        self.payload.pop('last_name')

        res = self.client.post(reverse("token"), self.payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', res.data)

    def test_token_refresh(self):
        """Testing token refresh."""

        refresh_token = self.test_user_login()['refresh']
        res = self.client.post(reverse('token-refresh'), {"refresh": refresh_token})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
