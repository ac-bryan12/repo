from django.contrib.auth.models import Group,Permission
from rest_framework import generics
from app.serializers.serializer_permission import GroupSerializer
from django.urls import path


class GroupViewSet(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermisosViewSet(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = GroupSerializer

urlpatterns = [
    path('grupos',GroupViewSet.as_view(), name = "Grupos"),
    path('permisos',PermisosViewSet.as_view(), name ="Permisos")
]