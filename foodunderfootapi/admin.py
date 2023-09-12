from django.contrib import admin
from foodunderfootapi.models.wild_plant import WildPlant
from foodunderfootapi.models import HarvestLog, PlantPart, Usability, TipsAndRecipes, EdiblePart

# Register your models here.
# import models here to be manipulated by admin

admin.site.register(WildPlant)
admin.site.register(HarvestLog)
admin.site.register(PlantPart)
admin.site.register(Usability)
admin.site.register(TipsAndRecipes)
admin.site.register(EdiblePart)


