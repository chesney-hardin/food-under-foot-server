from django.db import models


class Usability(models.Model):
    label = models.CharField(max_length=99)
    icon = models.CharField(max_length=99)

    def __str__(self) -> str:
        return f'{self.label}'
 