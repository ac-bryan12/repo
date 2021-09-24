from django.contrib.auth.models import Group,Permission, User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from app.serializers.serializer_permission import GroupSerializer,PermissionSerializer
from django.urls import path
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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

    def get(self,request,pk):
        admin = request.user
        if admin.user_permissions.filter(codename='view_user').exists() and admin.user_permissions.filter(codename='view_group').exists() and admin.user_permissions.filter(codename='view_permission').exists():
            empresa = admin.profile.empresa
            user = User.objects.filter(pk=pk)
            if user.exists():
                user = User.objects.get(pk=pk)
                if user.profile.empresa == empresa:
                    group = GroupSerializer(user.groups.all(),many=True)
                    permissions = PermissionSerializer(user.user_permissions.all(),many=True)
                    return Response({"groups":group.data,"permissions":permissions.data})
                else:
                    return Response({"msg":"Acceso denegado"})    
            else:
                return Response({"msg":"Usuario no existe"})
        else:
            return Response({"msg":"Acceso denegado"})    
urlpatterns = [
    path('grupos',GroupViewSet.as_view(), name = "Grupos"),
    path('permisos',PermisosViewSet.as_view(), name ="Permisos"),
    path('asignarPermisosRoles/',PermisosGruposViewSet.as_view()),
    path('getPermisosRoles/<int:pk>',PermisosGruposViewSet.as_view())
]