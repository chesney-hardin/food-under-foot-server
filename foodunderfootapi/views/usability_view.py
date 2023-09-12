from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodunderfootapi.models import Usability

class UsabilityView(ViewSet):
    """wild plant usability types view"""

    def list(self, request):
        """Handle GET requests to get all plant parts"""
        usability_types = Usability.objects.all()
        serialized = UsabilitySerializer(usability_types, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single plant part
        """
        usability_type = Usability.objects.get(pk=pk)
        serialized = UsabilitySerializer(usability_type)
        return Response(serialized.data, status=status.HTTP_200_OK)

class UsabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usability
        fields = ('id', 'label', 'icon')


