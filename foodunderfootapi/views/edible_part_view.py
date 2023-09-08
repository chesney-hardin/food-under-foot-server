from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import WildPlant, PlantPart, EdiblePart

class EdiblePartView(ViewSet):
    """wild plant profile view"""

    def list(self, request):
        """Handle GET requests to get all wild plants"""
        edible_parts = WildPlant.objects.all()
        serialized = WildPlantSerializer(edible_parts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single wild plant
        """
        wild_plant = WildPlant.objects.get(pk=pk)
        serialized = WildPlantSerializer(wild_plant)
        return Response(serialized.data, status=status.HTTP_200_OK)

class EdiblePartsOfPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ('id', 'label')

class WildPlantSerializer(serializers.ModelSerializer):
    """JSON serializer for wild plants"""
    class Meta:
        model = WildPlant
        fields = ('id', 'common_name', 'latin_name', 'alternate_names', 'latin_family', 'description', 'image', 'link_to_usda', 'created_by', 'edible_parts')

class EdiblePartSerializer(serializers.ModelSerializer):
    plant_part = EdiblePartsOfPlantSerializer(many=False)
    wild_plant = WildPlantSerializer(many=False)
    class Meta:
        model = PlantPart
        fields = ('id', 'wild_plant', 'plant_part', 'harvest_start', 'harvest_end', 'image')
        