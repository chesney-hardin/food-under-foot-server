from django.db import models
from django.contrib.auth.models import User


class WildPlant(models.Model):
    common_name = models.CharField(max_length=99)
    latin_name = models.CharField(max_length=99)
    alternate_names = models.CharField(max_length=299, null=True)
    latin_family = models.CharField(max_length=99)
    description = models.CharField(max_length=999)
    image = models.CharField(max_length=299)
    link_to_usda = models.CharField(max_length=299, null = True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    edible_parts = models.ManyToManyField("PlantPart", through="EdiblePart", related_name="plants_with_edible_part")    

    def __str__(self) -> str:
        return f'{self.common_name} ({self.latin_name})'
    