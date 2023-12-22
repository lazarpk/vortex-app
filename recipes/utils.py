from .models import Rate
from django.db.models import Avg
from .models import Recipe

def get_average_rate(recipe):
    return Rate.objects.filter(recipe=recipe).aggregate(Avg("rate"))["rate__avg"] or 0

def is_owner(request_user, recipe):
    recipe = Recipe.objects.get(id=recipe)
    if request_user == recipe.author:
        return True
    return False