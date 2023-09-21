from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import TipsAndRecipes, Favorite
from django.contrib.auth.models import User

class FavoriteView(ViewSet):
    """favorite view"""

    def list(self, request):
        """Handle GET requests to get all  parts"""
        favorites = Favorite.objects.all()
        serialized = FavoriteSerializer(favorites, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single  part
        """
        favorite = Favorite.objects.get(pk=pk)
        serialized = FavoriteSerializer(favorite)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class TipsAndRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipsAndRecipes
        fields = ('id', 'user', 'date', 'wild_plant', 'plant_part', 'title', 'description', 'image', 'isRecipe')

class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    tip_or_recipe= TipsAndRecipesSerializer(many=False)
    class Meta:
        model = Favorite
        fields = ('id', 'tip_or_recipe', 'user')


