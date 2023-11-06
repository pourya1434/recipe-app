from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse("recipe:recipe-list")


def create_recipe(user, **params):
    # default params
    default = {
        "title": "Awesome recipe",
        "time_minutes": 5,
        "price": Decimal("6.4"),
        "description": "Start and finish with paitions",
        "link": "https://example.com/recipe.pdf",
    }
    # update params with new one
    default.update(params)

    recipe = Recipe.objects.create(user=user, **default)
    return recipe


class PublicRecipeApiTest(TestCase):
    """test unauthenticated api request"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@example.com", "testpassword123"
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_list_limited_to_user(self):
        other_user = get_user_model().objects.create_user(
            "otheruser@example.com", "otheruserpass"
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recepies = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recepies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
