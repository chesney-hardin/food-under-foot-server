from django.db import models


class PlantPart(models.Model):
    label = models.CharField(max_length=99)

    def __str__(self) -> str:
        return f'{self.label}'
 