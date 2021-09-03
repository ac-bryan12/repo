from django.contrib.auth.models import Group
from rest_framework import generics, status
from app.serializers.serializer_permission import GroupSerializer
from rest_framework.response import Response
from django.urls import path


class GroupViewSet(generics.ListAPIView):
    serializer_class =  GroupSerializer
    
    def post(self, request,pk, format=None):
        if request.user.is_superuser:
            serializer = GroupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)   

urlpatterns = [
    path('selecion-de-grupo/',GroupViewSet.as_view(), name = "Grupos"),
]