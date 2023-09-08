from django.db import models
from django.contrib.auth.models import User


class TipsAndRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    edible_part = models.ForeignKey("EdiblePart", on_delete=models.CASCADE)
    title = models.CharField(max_length=199)
    description = models.CharField(max_length=999)
    image = models.CharField(max_length=299)
    isRecipe = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)
