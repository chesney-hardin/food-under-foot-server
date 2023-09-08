from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import WildPlant, PlantPart, HarvestLog
from django.contrib.auth.models import User


class HarvestLogView(ViewSet):
    """harvest log profile view"""

    def list(self, request):
        """Handle GET requests to get all harvest logs"""
        harvest_logs = HarvestLog.objects.all()
        serialized = HarvestLogSerializer(harvest_logs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single harvest log
        """
        harvest_log = HarvestLog.objects.get(pk=pk)
        serialized = HarvestLogSerializer(harvest_log)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username')

class EdiblePartsOfPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ('id', 'label')

class WildPlantSerializer(serializers.ModelSerializer):
    """JSON serializer for wild plants"""
    class Meta:
        model = WildPlant
        fields = ('id', 'common_name', 'latin_name', 'alternate_names', 'latin_family', 'description', 'image', 'link_to_usda', 'created_by', 'edible_parts')

class HarvestLogSerializer(serializers.ModelSerializer):
    """JSON serializer for harvest logs"""
    user = UserSerializer(many=False)
    wild_plant= WildPlantSerializer(many=False)
    plant_part = EdiblePartsOfPlantSerializer(many=False)
    class Meta:
        model = HarvestLog
        fields = ('id', 'user', 'date', 'wild_plant', 'plant_part', 'latitude', 'longitude', 'isPublicLocation', 'quantity', 'title', 'description', 'image', 'isPublic')

    