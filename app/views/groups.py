from django.contrib.auth.models import Group,Permission
from rest_framework import generics
from rest_framework.views import APIView
from app.serializers.serializer_permission import GroupSerializer
from django.urls import path
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class GroupViewSet(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermisosViewSet(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = GroupSerializer

class PermisosGruposViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user= request.user
        user.user_permissions.add(
            Permission.objects.get()
        )
   

urlpatterns = [
    path('grupos',GroupViewSet.as_view(), name = "Grupos"),
    path('permisos',PermisosViewSet.as_view(), name ="Permisos"),
    path('asignarPermisosRoles',PermisosGruposViewSet.as_view())
]