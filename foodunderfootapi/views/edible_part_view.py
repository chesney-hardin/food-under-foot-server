from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
import datetime
from foodunderfootapi.models import WildPlant, PlantPart, EdiblePart, Usability

class EdiblePartView(ViewSet):
    """wild plant profile view"""

    def list(self, request):
        """Handle GET requests to get all wild plants"""
        edible_parts = EdiblePart.objects.all()

        usability = request.query_params.get('usability', None)

        if usability is not None:
            edible_parts =  edible_parts.filter(usability__id=usability)

        if "current" in request.query_params:
            current_month = datetime.datetime.now().strftime("%m")
            current_start= edible_parts.filter(harvest_start__lte = current_month)
            current_end = current_start.filter(harvest_end__gte = current_month)
            edible_parts = current_end
        if "plant" in request.query_params:
            pk = request.query_params['plant']
            edible_parts = edible_parts.filter(wild_plant = pk)
        

        serialized = EdiblePartSerializer(edible_parts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single wild plant
        """
        edible_part = EdiblePart.objects.get(pk=pk)
        serialized = EdiblePartSerializer(edible_part)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
        
    def create(self, request):
        """Handle POST requests to add an edible part to a plant"""
        wild_plant = WildPlant.objects.get(pk=request.data["wild_plant"])
        plant_part = PlantPart.objects.get(pk=request.data["plant_part"])
        usability = Usability.objects.get(pk=request.data["usability"])

        edible_part = EdiblePart.objects.create(
            wild_plant = wild_plant,
            plant_part = plant_part,
            usability = usability,
            harvest_start = request.data["harvest_start"],
            harvest_end = request.data["harvest_end"],
            image= request.data["image"]
        )
        serialized = EdiblePartSerializer(edible_part)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        """Delete an edible part"""
        try:
            edible_part = EdiblePart.objects.get(pk=pk)
            edible_part.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except EdiblePart.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk):
        """Update an edible part"""
        edible_part = EdiblePart.objects.get(pk=pk)

        edible_part.wild_plant = WildPlant.objects.get(pk=request.data["wild_plant"])
        edible_part.plant_part = PlantPart.objects.get(pk=request.data["plant_part"])
        edible_part.usability = Usability.objects.get(pk=request.data["usability"])
        edible_part.harvest_start = request.data["harvest_start"]
        edible_part.harvest_end = request.data["harvest_end"]
        edible_part.image = request.data["image"]

        edible_part.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class EdiblePartsOfPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPart
        fields = ('id', 'label')

class WildPlantSerializer(serializers.ModelSerializer):
    """JSON serializer for wild plants"""
    class Meta:
        model = WildPlant
        fields = ('id', 'common_name', 'latin_name', 'alternate_names', 'latin_family', 'description', 'image', 'link_to_usda', 'created_by', 'edible_parts')

class UsabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usability
        fields = ('id', 'label', 'icon')

class EdiblePartSerializer(serializers.ModelSerializer):

    plant_part = EdiblePartsOfPlantSerializer(many=False)
    wild_plant = WildPlantSerializer(many=False)
    usability = UsabilitySerializer(many=False)
    class Meta:
        model = EdiblePart
        fields = ('id', 'wild_plant', 'plant_part', 'usability', 'harvest_start', 'harvest_end', 'image')
        