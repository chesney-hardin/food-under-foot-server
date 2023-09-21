from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    tip_or_recipe = models.ForeignKey("TipsAndRecipes", on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
