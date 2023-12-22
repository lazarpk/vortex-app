from django.urls import path
from .views import (
    CreateIngredient,
    CreateRecipe,
    ListRecipes,
    ListOwnRecipes,
    RateRecipe,
    MostUsedIngredients
)

urlpatterns = [
    path('ingredient/create', CreateIngredient.as_view(), name='create-ingredient'),
    path('ingredient/most-used', MostUsedIngredients.as_view(), name='most-used'),
    path('recipe/create', CreateRecipe.as_view(), name='create-recipe'),
    path('recipe/list', ListRecipes.as_view(), name='list-recipe'),
    path('recipe/list/own', ListOwnRecipes.as_view(), name='list-own-recipe'),
    path('recipe/rate', RateRecipe.as_view(), name='rate-recipe'),
]
