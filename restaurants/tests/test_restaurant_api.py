from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from restaurants.models import Restaurant

CREATE_RESTAURANT_URL = reverse("restaurants:restaurant-list")
UPDATE_RESTAURANT_URL = lambda pk: reverse(
    "restaurants:restaurant-detail", kwargs={"pk": pk}
)
DELETE_RESTAURANT_URL = lambda pk: reverse(
    "restaurants:restaurant-detail", kwargs={"pk": pk}
)


def create_user(**params):
    """Helper function to create a new user"""
    return get_user_model().objects.create_superuser(**params)


class RestaurantAPITests(TestCase):
    """Test the restaurants API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com",
            password="testpass123",
        )
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        res = self.client.post(reverse("users:token_obtain_pair"), payload)
        self.token = res.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
        )

    def test_create_restaurant(self):
        """Test creating a restaurant"""
        payload = {
            "name": "New Restaurant",
        }
        res = self.client.post(CREATE_RESTAURANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])

    def test_get_restaurant_list(self):
        """Test retrieving a list of restaurants"""
        res = self.client.get(CREATE_RESTAURANT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], self.restaurant.name)

    def test_get_single_restaurant(self):
        """Test retrieving a single restaurant"""
        url = UPDATE_RESTAURANT_URL(self.restaurant.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.restaurant.name)

    def test_update_restaurant(self):
        """Test updating a restaurant"""
        url = UPDATE_RESTAURANT_URL(self.restaurant.id)
        payload = {
            "name": "Updated Restaurant",
        }
        res = self.client.patch(url, payload)

        self.restaurant.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.restaurant.name, payload["name"])

    def test_delete_restaurant(self):
        """Test deleting a restaurant"""
        url = DELETE_RESTAURANT_URL(self.restaurant.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Restaurant.objects.filter(id=self.restaurant.id).exists()
        )
