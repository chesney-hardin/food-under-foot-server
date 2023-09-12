from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import WildPlant, PlantPart

class PlantPartView(ViewSet):
    """wild plant profile view"""

    def list(self, request):
        """Handle GET requests to get all plant parts"""
        plant_parts = PlantPart.objects.all()
        serialized = PlantPartSerializer(plant_parts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single plant part
        """
        plant_part = PlantPart.objects.get(pk=pk)
        serialized = PlantPartSerializer(plant_part)
        return Response(serialized.data, status=status.HTTP_200_OK)

class PlantPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ('id', 'label')


