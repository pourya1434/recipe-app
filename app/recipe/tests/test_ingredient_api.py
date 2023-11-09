from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse("recipe:ingredient-list")


def create_user(email="uesr@example.com", password="userpass"):
    return get_user_model().objects.create_user(email=email, password=password)


def detail_url(ingredient_id):
    """Retrive ingredient detail url"""
    return reverse("recipe:ingredient-detail", args=[ingredient_id])


class PublicIngredientApiTest(TestCase):
    """Test for unauthenticated users"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_ingredient(self):
        """Test rereive list of ingredients"""
        Ingredient.objects.create(user=self.user, name="Vanilla")
        Ingredient.objects.create(user=self.user, name="Kale")

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limit_to_user(self):
        """Test List of ingredients limited to authenticated user"""
        user2 = create_user(email="user2@gmail.com", password="user2pass")
        Ingredient.objects.create(user=user2, name="salt")
        ingredient = Ingredient.objects.create(user=self.user, name="papper")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)
        self.assertEqual(res.data[0]["id"], ingredient.id)
