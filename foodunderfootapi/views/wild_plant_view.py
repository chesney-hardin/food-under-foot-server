from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import WildPlant, PlantPart
from django.contrib.auth.models import User


class WildPlantView(ViewSet):
    """wild plant profile view"""

    def list(self, request):
        """Handle GET requests to get all wild plants"""
        wild_plants = WildPlant.objects.order_by('common_name')

        name_search = request.query_params.get('common_name', None)
        edible_part = request.query_params.get('edible_part', None)
        

        if name_search is not None:
            wild_plants = wild_plants.filter(common_name__icontains=name_search)

        if edible_part is not None:
            wild_plants = wild_plants.filter(edible_parts__id=edible_part)

        serialized = WildPlantSerializer(wild_plants, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single wild plant
        """
        wild_plant = WildPlant.objects.get(pk=pk)
        serialized = WildPlantSerializer(wild_plant)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests to create a new wild plant"""
        wild_plant = WildPlant.objects.create(
            common_name=request.data["common_name"],
            latin_name=request.data["latin_name"],
            alternate_names=request.data["alternate_names"],
            latin_family=request.data["latin_family"],
            description=request.data["description"],
            image=request.data["image"],
            link_to_usda=request.data["link_to_usda"],
            created_by=request.auth.user
        )
        serialized = WildPlantSerializer(wild_plant)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """Delete a wild plant"""
        try:
            wild_plant = WildPlant.objects.get(pk=pk)
            wild_plant.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except WildPlant.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):
        """Update a wild plant"""
        wild_plant = WildPlant.objects.get(pk=pk)

        wild_plant.common_name = request.data["common_name"]
        wild_plant.latin_name = request.data["latin_name"]
        wild_plant.alternate_names = request.data["alternate_names"]
        wild_plant.latin_family = request.data["latin_family"]
        wild_plant.description = request.data["description"]
        wild_plant.image = request.data["image"]
        wild_plant.link_to_usda = request.data["link_to_usda"]
        wild_plant.created_by = User.objects.get(pk=request.data['created_by'])

        wild_plant.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class EdiblePartsOfPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ('id', 'label')


class WildPlantSerializer(serializers.ModelSerializer):
    """JSON serializer for wild plants"""
    edible_parts = EdiblePartsOfPlantSerializer(many=True)
    class Meta:
        model = WildPlant
        fields = ('id', 'common_name', 'latin_name', 'alternate_names', 'latin_family',
                'description', 'image', 'link_to_usda', 'created_by', 'edible_parts')
