from rest_framework import serializers
from .models import Ingredient, Recipe, Rate
from django.db.models import Count
from .utils import get_average_rate, is_owner


class CreateIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ['name']

class MostUsedIngredientsSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('name', 'count')

    def get_name(self, obj):
        ingredient = Ingredient.objects.get(id=obj['ingredients'])
        return ingredient.name

class CreateRecipeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'ingredients', 'author')

class ListRecipeSerializer(serializers.ModelSerializer):
    ingredients = CreateIngredientSerializer(many=True)
    author = serializers.CharField(source='author.email')
    rate = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'ingredients', 'author', 'rate')

    def get_rate(self, obj):
        return round(get_average_rate(obj.pk), 2)
    
class RateRecipeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Rate
        fields = ('recipe', 'rate', 'user')

    def validate(self, data):
        if is_owner(self.context['request'].user, data.get('recipe').id):
            raise serializers.ValidationError(
                {"error": "You cannot rate your own recipes!"}
            )
        
        rate = data.get('rate')
        if rate > 5 or rate < 1:
            raise serializers.ValidationError(
                {"rate": "Rate must be between 1 and 5."}
            )
        return data