from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from users.models import Employee
from restaurants.models import Restaurant, Menu
from votes.models import Vote


class VoteAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.user = Employee.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )
        self.superuser = Employee.objects.create_superuser(
            email="superuser@example.com", password="superpass123"
        )

        self.restaurant = Restaurant.objects.create(name="Test Restaurant")
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            date="2025-02-14",
            items="Dish 1, Dish 2",
        )

        self.employee = Employee.objects.create(
            email="employee@example.com", password="employeepass123"
        )

        payload = {"email": "testuser@example.com", "password": "testpass123"}
        res = self.client.post(reverse("users:token_obtain_pair"), payload)
        self.token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_vote(self):
        url = reverse("votes:vote-list")
        payload = {"menu": self.menu.id}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_vote_wrong_menu_date(self):
        wrong_menu = Menu.objects.create(
            restaurant=self.restaurant,
            date="2025-02-13",
            items="Dish 3, Dish 4",
        )
        url = reverse("votes:vote-list")
        payload = {"menu": wrong_menu.id}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_vote_as_admin(self):
        vote = Vote.objects.create(employee=self.employee, menu=self.menu)
        self.client.force_authenticate(user=self.superuser)
        url = reverse("votes:vote-detail", args=[vote.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_vote_as_user(self):
        vote = Vote.objects.create(employee=self.employee, menu=self.menu)
        url = reverse("votes:vote-detail", args=[vote.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_vote_list(self):
        Vote.objects.create(employee=self.employee, menu=self.menu)
        url = reverse("votes:vote-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_vote_list_as_admin(self):
        Vote.objects.create(employee=self.employee, menu=self.menu)
        self.client.force_authenticate(user=self.superuser)
        url = reverse("votes:vote-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
