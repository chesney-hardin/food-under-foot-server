from django.db import models
from django.contrib.auth.models import User


class Favorite(models.Model):
    wild_plant = models.ForeignKey("WildPlant", on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
