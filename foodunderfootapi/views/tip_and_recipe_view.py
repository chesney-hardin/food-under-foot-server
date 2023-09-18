from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import TipsAndRecipes, EdiblePart, WildPlant, PlantPart
from django.contrib.auth.models import User


class TipsAndRecipesView(ViewSet):
    """tips and recipes view"""

    def list(self, request):
        """Handle GET requests to get all tips and recipes"""
        tips_and_recipes = TipsAndRecipes.objects.order_by('date')

        approved = request.query_params.get('approved', None)
        unapproved = request.query_params.get('unapproved', None)
        recipes = request.query_params.get('recipes', None)
        tips = request.query_params.get('tips', None)
        plant = request.query_params.get('plant', None)
        user = request.query_params.get('user', None)

        if approved is not None:
            tips_and_recipes = tips_and_recipes.filter(isApproved=True)

        if unapproved is not None:
            tips_and_recipes = tips_and_recipes.filter(isApproved=False)

        if recipes is not None:
            tips_and_recipes = tips_and_recipes.filter(isRecipe=True)

        if tips is not None:
            tips_and_recipes = tips_and_recipes.filter(isRecipe=False)

        if plant is not None:
            tips_and_recipes = tips_and_recipes.filter(wild_plant__id=plant)

        if user is not None:
            tips_and_recipes = tips_and_recipes.filter(user=request.auth.user)

        serialized = TipsAndRecipesSerializer(tips_and_recipes, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single plant part
        """
        tip_or_recipe = TipsAndRecipes.objects.get(pk=pk)
        serialized = TipsAndRecipesSerializer(tip_or_recipe)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests to add a tip or recipe"""

        tip_or_recipe = TipsAndRecipes.objects.create(
            user=request.auth.user,
            wild_plant=WildPlant.objects.get(pk=request.data["wild_plant"]),
            plant_part=PlantPart.objects.get(pk=request.data["plant_part"]),
            title=request.data["title"],
            description=request.data["description"],
            image=request.data["image"],
            isRecipe=request.data["isRecipe"],
            isApproved=request.data["isApproved"],
            needsReview=request.data["needsReview"],
            reasonUnapproved=request.data["reasonUnapproved"]
        )
        serialized = TipsAndRecipesSerializer(tip_or_recipe)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Update a tip or recipe"""
        tip_or_recipe = TipsAndRecipes.objects.get(pk=pk)

        tip_or_recipe.user = User.objects.get(pk=request.data['user'])
        tip_or_recipe.wild_plant = WildPlant.objects.get(
            pk=request.data["wild_plant"])
        tip_or_recipe.plant_part = PlantPart.objects.get(
            pk=request.data["plant_part"])
        tip_or_recipe.date = request.data['date']
        tip_or_recipe.title = request.data['title']
        tip_or_recipe.description = request.data["description"]
        tip_or_recipe.image = request.data["image"]
        tip_or_recipe.isRecipe = request.data["isRecipe"]
        tip_or_recipe.isApproved = request.data["isApproved"]
        tip_or_recipe.needsReview = request.data["needsReview"]
        tip_or_recipe.reasonUnapproved = request.data["reasonUnapproved"]

        tip_or_recipe.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Delete a tip or recipe"""
        try:
            tip_or_recipe = TipsAndRecipes.objects.get(pk=pk)
            tip_or_recipe.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except TipsAndRecipes.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        


class WildPlantSerializer(serializers.ModelSerializer):
    """JSON serializer for wild plants"""
    class Meta:
        model = WildPlant
        fields = ('id', 'common_name', 'latin_name', 'alternate_names', 'latin_family', 'description', 'image', 'link_to_usda', 'created_by', 'edible_parts')


class EdiblePartsOfPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ('id', 'label')

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class TipsAndRecipesSerializer(serializers.ModelSerializer):
    wild_plant= WildPlantSerializer(many=False)
    plant_part = EdiblePartsOfPlantSerializer(many=False)
    user = UserSerializer(many=False)
    class Meta:
        model = TipsAndRecipes
        fields = ('id', 'user', 'date', 'wild_plant', 'plant_part', 'title', 'description', 'image', 'isRecipe', 'isApproved', 'needsReview', 'reasonUnapproved')

