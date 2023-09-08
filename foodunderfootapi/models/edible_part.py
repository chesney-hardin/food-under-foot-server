from django.db import models


class EdiblePart(models.Model):
    wild_plant = models.ForeignKey("WildPlant", on_delete=models.CASCADE)
    plant_part = models.ForeignKey("PlantPart", on_delete=models.CASCADE, related_name='edible_parts')
    harvest_start = models.CharField(max_length=5) # Only accepts "MM-DD"
    harvest_end = models.CharField(max_length=5) # Only accepts "MM-DD"
    image = models.CharField(max_length=299)
