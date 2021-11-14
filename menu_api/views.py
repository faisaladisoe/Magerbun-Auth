from django.shortcuts import render
from rest_framework.views import APIView
from menu_api.models import Menu
from menu_api.serializers import MenuSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

# Create your views here.

@permission_classes([IsAuthenticated|IsAdminUser])
class MenuList(APIView):
    def get(self, request, format=None):
        menu = Menu.objects.all()
        serializers = MenuSerializer(menu, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated|IsAdminUser])
class MenuDetail(APIView):
    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        menu = self.get_object(pk)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
