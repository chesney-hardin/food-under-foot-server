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
        harvest_logs = HarvestLog.objects.order_by('date')

        title_search = request.query_params.get('title', None)

        if title_search is not None:
            harvest_logs = harvest_logs.filter(title__icontains=title_search)

        if "public" in request.query_params:
            harvest_logs = harvest_logs.filter(isPublic = True)
            if "plant" in request.query_params:
                pk= request.query_params['plant']
                harvest_logs = harvest_logs.filter(wild_plant=pk)
        if "user" in request.query_params:
            harvest_logs = harvest_logs.filter(user=request.auth.user)

        serialized = HarvestLogSerializer(harvest_logs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single harvest log
        """
        harvest_log = HarvestLog.objects.get(pk=pk)
        serialized = HarvestLogSerializer(harvest_log)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST requests to add an edible part to a plant"""

        harvest_log = HarvestLog.objects.create(
            user = request.auth.user,
            wild_plant = WildPlant.objects.get(pk=request.data["wild_plant"]),
            plant_part = PlantPart.objects.get(pk=request.data["plant_part"]),
            date = request.data['date'],
            longitude = request.data['longitude'],
            latitude = request.data['latitude'],
            isPublicLocation = request.data["isPublicLocation"],
            quantity = request.data["quantity"],
            title = request.data["title"],
            description = request.data["description"],
            image= request.data["image"],
            isPublic = request.data["isPublic"]
        )
        serialized = HarvestLogSerializer(harvest_log)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """Delete a harvest log"""
        try:
            harvest_log = HarvestLog.objects.get(pk=pk)
            harvest_log.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except WildPlant.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk):
        """Update a harvest log"""
        harvest_log = HarvestLog.objects.get(pk=pk)

        harvest_log.wild_plant = WildPlant.objects.get(pk=request.data["wild_plant"])
        harvest_log.plant_part = PlantPart.objects.get(pk=request.data["plant_part"])
        harvest_log.date = request.data['date']
        harvest_log.longitude = request.data['longitude']
        harvest_log.latitude = request.data['latitude']
        harvest_log.isPublicLocation = request.data['isPublicLocation']
        harvest_log.quantity = request.data['quantity']
        harvest_log.title = request.data['title']
        harvest_log.description = request.data["description"]
        harvest_log.image = request.data["image"]
        harvest_log.isPublic = request.data["isPublic"]
        harvest_log.user = User.objects.get(pk=request.data['user'])

        harvest_log.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    
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

    