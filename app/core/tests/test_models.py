from django.test import TestCase
from django.contrib.auth import get_user_model

from decimal import Decimal
from core import models
from unittest.mock import patch


def create_user(email="testuser@example.com", password="testpassword"):
    """Create and return new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpassword123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )  # create user --> UserManager --> default method

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        """Every Register user must have an email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "sample123")

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            "test@example.com", "testpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            "testuser@example.com", "testpassword"
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Some recipe description.",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tags(self):
        """Test creating tags successfully"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user, name="Ingredient1"
        )  # long line

        self.assertEqual(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
