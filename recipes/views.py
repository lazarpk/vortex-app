from django.shortcuts import render
from rest_framework import mixins, generics, permissions, filters
from .models import Ingredient, Recipe, Rate
from django.db.models import Count
from .serializers import (
    CreateIngredientSerializer, 
    CreateRecipeSerializer,
    ListRecipeSerializer,
    RateRecipeSerializer,
    MostUsedIngredientsSerializer
)

class CreateIngredient(mixins.CreateModelMixin, generics.GenericAPIView):
    """Create certain ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = CreateIngredientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class MostUsedIngredients(mixins.ListModelMixin, generics.GenericAPIView):
    """List 5 most used ingredients in recipes."""

    queryset = Ingredient.objects.prefetch_related("ingredients").all()
    serializer_class = MostUsedIngredientsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Recipe.objects.values('ingredients').annotate(count=Count('ingredients')).order_by('-count')[:5]
        return queryset
    
class CreateRecipe(mixins.CreateModelMixin, generics.GenericAPIView):
    """Create recipe API."""

    queryset = Recipe.objects.all()
    serializer_class = CreateRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ListRecipes(mixins.ListModelMixin, generics.GenericAPIView):
    """List all recipes."""

    queryset = Recipe.objects.prefetch_related("ingredients").all()
    serializer_class = ListRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "text", "ingredients__name",)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Recipe.objects.prefetch_related("ingredients").all()

        max_ingredients = self.request.query_params.get("max_ingredients", None)
        min_ingredients = self.request.query_params.get("min_ingredients", None)

        if max_ingredients:
            queryset = queryset.annotate(total=Count('ingredients')).filter(total__lte=int(max_ingredients))
        if min_ingredients:
            queryset = queryset.annotate(total=Count("ingredients")).filter(total__gte=int(min_ingredients))
        return queryset
    
class ListOwnRecipes(mixins.ListModelMixin, generics.GenericAPIView):
    """List own recipes."""

    queryset = Recipe.objects.prefetch_related("ingredients").all()
    serializer_class = ListRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Recipe.objects.prefetch_related("ingredients").filter(author=self.request.user)
        return queryset

class RateRecipe(mixins.CreateModelMixin, generics.GenericAPIView):
    """Rate others recipe."""

    queryset = Rate.objects.select_related("user").all()
    serializer_class = RateRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

