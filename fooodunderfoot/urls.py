from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from foodunderfootapi.views import register_user, login_user, FavoriteView, TipsAndRecipesView, UserView, EdiblePartView, HarvestLogView, PlantPartView, WildPlantView, UsabilityView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'harvestlogs', HarvestLogView, 'harvestlog')
router.register(r'plantparts', PlantPartView, 'plantpart')
router.register(r'wildplants', WildPlantView, 'wildplant')
router.register(r'edibleparts', EdiblePartView, 'ediblepart')
router.register(r'usabilitytypes', UsabilityView, 'usabilitytype')
router.register(r'users', UserView, 'user')
router.register(r'tipsandrecipes', TipsAndRecipesView, 'tipandrecipe')
router.register(r'favoriteplants', FavoriteView, 'favoriteplant')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]