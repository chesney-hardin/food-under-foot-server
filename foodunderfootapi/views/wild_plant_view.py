from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import WildPlant, PlantPart

class WildPlantView(ViewSet):
    """wild plant profile view"""

    def list(self, request):
        """Handle GET requests to get all wild plants"""
        wild_plants = WildPlant.objects.all()
        serialized = WildPlantSerializer(wild_plants, many=True)
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
    edible_parts = EdiblePartsOfPlantSerializer(many=True)
    class Meta:
        model = WildPlant
        fields = ('id', 'common_name', 'latin_name', 'alternate_names', 'latin_family', 'description', 'image', 'link_to_usda', 'created_by', 'edible_parts')



