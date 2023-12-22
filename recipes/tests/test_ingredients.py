from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

def create_user(first_name="John", last_name="Doe", email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)

class PublicIngredientsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for creating ingredients."""
        res = self.client.get(reverse("create-ingredient"))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsAPITests(TestCase):
    """Test ingredient API."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.payload = {
            "name": "So"
        }

    def test_adding_ingredient_success(self):
        """Testing adding ingredient is successful."""

        res = self.client.post(reverse("create-ingredient"), self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.payload['name'], res.data['name'])