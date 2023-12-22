from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe
from recipes.serializers import ListRecipeSerializer
import json

def create_user(first_name="John", last_name="Doe", email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password)

def create_ingredient(**params):
    """Create and return ingredient."""
    return Ingredient.objects.create(**params)

def create_recipe(author):
    """Create and return a sample recipe."""
    ingredient = create_ingredient(name="So")

    defaults = {
        "name": "Test",
        "text": "Test text",
    }

    recipe = Recipe.objects.create(author=author, **defaults)
    recipe.ingredients.add(ingredient.id)
    return recipe

class RecipeAPITests(TestCase):
    """Test recipe API."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.payload = {
            "name": "Proja",
            "text": "Proja je jelo koje se pravi od jaja, brasna i soli.",
            "ingredients": [1, 2]
        }

    def test_creating_recipe_successful(self):
        """Test creating recipe is successful."""

        create_ingredient(name="So")
        create_ingredient(name="Voda")

        res = self.client.post(reverse("create-recipe"), self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_creating_recipe_error(self):
        """Test creating recipe without ingredients results with error."""

        self.payload["ingredients"] = []
        res = self.client.post(reverse("create-recipe"), self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_recipes_success(self):
        """Test listing recipes successful."""

        res = self.client.get(reverse('list-recipe'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_own_recipes(self):
        """Test list of recipes is limited to authenticated user."""

        other_user = create_user(email='other@example.com', password='test123')
        create_recipe(author=other_user)
        create_recipe(author=self.user)

        res = self.client.get(reverse('list-own-recipe'))

        recipes = Recipe.objects.filter(author=self.user)
        serializer = ListRecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_rating_recipe_success(self):
        """Test rating recipe is successful."""

        other_user = create_user(email='other@example.com', password='test123')
        recipe = create_recipe(author=other_user)

        payload = {
            "recipe": recipe.id,
            "rate": 5 
        }

        res = self.client.post(reverse('rate-recipe'), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_rate_own_recipes_error(self):
        """Testing rating own recipes results with error."""

        recipe = create_recipe(author=self.user)
        payload = {
            "recipe": recipe.id,
            "rate": 3
        }

        res = self.client.post(reverse('rate-recipe'), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", res.data)

    def test_search_recipes(self):
        """Testing searching recipes by name, text or ingredient."""

        recipe = create_recipe(self.user)

        name = recipe.name
        res = self.client.get(f'{reverse("list-recipe")}?search={name}')
        response = json.loads(json.dumps(res.data))[0]


        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(response['name'], name)

    def test_filtering_recipes_maximum_and_minimum(self):
        """Testing filtering recipes by maximum or minimum number of ingredients."""

        salt = create_ingredient(name="So")
        water = create_ingredient(name="Voda")
        flour = create_ingredient(name="Brasno")
        eggs = create_ingredient(name="Jaja")
        cheese = create_ingredient(name="Sir")

        first_recipe = {
            "name": "Kacamak",
            "text": "Kacamak je jelo koje se pravi od vode, brasna i soli.",
            "ingredients": [salt.id, water.id, flour.id]
        }
        second_recipe = {
            "name": "Pita",
            "text": "Pita je jelo koje se pravi od kora, sira i jaja.",
            "ingredients": [eggs.id, cheese.id]
        }

        self.client.post(reverse("create-recipe"), first_recipe)
        self.client.post(reverse("create-recipe"), second_recipe)

        res_max = self.client.get(f'{reverse("list-recipe")}?max_ingredients=3')
        res__max_count = len(json.loads(json.dumps(res_max.data)))

        self.assertEqual(res_max.status_code, status.HTTP_200_OK)
        self.assertEqual(res__max_count, 2)

        res_min = self.client.get(f'{reverse("list-recipe")}?min_ingredients=3')
        res_min_count = len(json.loads(json.dumps(res_min.data)))

        self.assertEqual(res_min.status_code, status.HTTP_200_OK)
        self.assertEqual(res_min_count, 1)
        
