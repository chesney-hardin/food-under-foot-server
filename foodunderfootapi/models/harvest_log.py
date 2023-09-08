from django.db import models
from django.contrib.auth.models import User


class HarvestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    wild_plant = models.ForeignKey("WildPlant", on_delete=models.CASCADE, related_name='harvest_logs')
    plant_part = models.ForeignKey("PlantPart", on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    isPublicLocation = models.BooleanField(default=False)
    quantity = models.CharField(max_length=199)
    title = models.CharField(max_length=199)
    description = models.CharField(max_length=999)
    image = models.CharField(max_length=299)
    isPublic = models.BooleanField(default=False)
