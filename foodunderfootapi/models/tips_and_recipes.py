from django.db import models
from django.contrib.auth.models import User


class TipsAndRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    wild_plant = models.ForeignKey("WildPlant", on_delete=models.CASCADE)
    plant_part = models.ForeignKey("PlantPart", on_delete=models.CASCADE)
    title = models.CharField(max_length=199)
    description = models.CharField(max_length=999)
    image = models.CharField(max_length=299)
    isRecipe = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)
    needsReview = models.BooleanField(default=True)
    reasonUnapproved = models.CharField(max_length=999, default=None)

    def __str__(self) -> str:
        return f'{self.title}'
