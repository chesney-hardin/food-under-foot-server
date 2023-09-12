from django.db import models


class EdiblePart(models.Model):
    wild_plant = models.ForeignKey("WildPlant", on_delete=models.CASCADE)
    plant_part = models.ForeignKey("PlantPart", on_delete=models.CASCADE)
    usability = models.ForeignKey("Usability", on_delete=models.DO_NOTHING)
    harvest_start = models.CharField(max_length=2) # Only accepts "MM"
    harvest_end = models.CharField(max_length=2) # Only accepts "MM"
    image = models.CharField(max_length=299)

    def __str__(self) -> str:
        return f'Plant:{self.wild_plant} Part:{self.plant_part}'
