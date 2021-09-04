from app.models.profile import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from app.models.empresa import Empresa
from rest_framework import serializers, permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from app.models.plan import Plan
from django.http import Http404
from django.urls import path
from rest_framework.authentication import TokenAuthentication


class planSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['nombre','precio','description','documentos','reportes','soporte','firma','usuarios','clientes']

class planViewSet(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = planSerializer

class empresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class listEmpresaViewSet(generics.ListAPIView):
    queryset = Empresa.objects.all()
    serializer_class = empresaSerializer

class empresaViewSet(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = empresaSerializer
    def validarCodigoVerificacion(self,token):
        try:
            if Token.objects.filter(key=token).exists() :
                return True
            else:
                print
                return False
        except:
            return False
    def validarSuperUser(self,token):
        try:
            t = Token.objects.get(key=token)
            if User.objects.get(id= t.user_id).is_superuser:
                return True
            else:
                return False
        except User.DoesNotExist:
            raise False
        except: 
            return False

    def get_object(self, pk):
        try:
            return Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            raise Http404

    def get(self, request,format=None):

# if 'Authorization' in request.headers.keys():
    # token:str = request.headers.get('Authorization')
    # token = token.removeprefix('Token ')
    # if self.validarCodigoVerificacion(token) & self.validarSuperUser(token) :
        profile:Profile = request.user.profile
        serializer = empresaSerializer(profile.empresa)
        return Response(serializer.data)
    # else:
    #     return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)
# else:
#     return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)

    # def post(self, request,pk, format=None):
    #     if request.user.is_superuser:
    #         serializer = empresaSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    #     else:
    #         return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)   

    def put(self, request, pk, format=None):
        if 'Authorization' in request.headers.keys():
            token:str = request.headers.get('Authorization')
            token = token.removeprefix('Token ')
            if self.validarCodigoVerificacion(token) & self.validarSuperUser(token) :
                empresa = self.get_object(self,pk)
                serializer = empresaSerializer(empresa, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)   

    def delete(self, request, pk, format=None):
        if 'Authorization' in request.headers.keys():
            token:str = request.headers.get('Authorization')
            token = token.removeprefix('Token ')
            if self.validarCodigoVerificacion(token) & self.validarSuperUser(token) :
                empresa = self.get_object(pk)
                empresa.active = False
                empresa.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)      


urlpatterns = [
    path('planes.format.json/',planViewSet.as_view()),
    path('empresas/buscar-empresa/',empresaViewSet.as_view(), name = "Empresa"),
    path('empresas/lista-de-empresas/', listEmpresaViewSet.as_view())
]

