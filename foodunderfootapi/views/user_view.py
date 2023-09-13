from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User

class UserView(ViewSet):
    """django user model view"""
    def list(self, request):
        """Handle GET requests to get all users"""
        users = User.objects.all()
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single user
        """
        user = User.objects.get(pk=pk)
        serialized = UserSerializer(user)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        """update user's information"""
        user = User.objects.get(pk=pk)

        user.username = request.data['username']
        user.email = request.data['email']
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.password = request.data['password']

        user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
