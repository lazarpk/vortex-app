from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg

class Ingredient(models.Model):
    name = models.CharField(max_length=25)

class Recipe(models.Model):
    name = models.CharField(max_length=55)
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='ingredients')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @property
    def average_rating(recipe):
        return Rate.objects.filter(recipe=recipe).aggregate(Avg("rate"))["rate__avg"] or 0

class Rate(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rate = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

