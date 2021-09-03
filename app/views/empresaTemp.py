from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from app.models.empresaTemp import  EmpresaTemp
from rest_framework import  permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import Http404
from django.urls import path
from app.serializers.serializer_empresaTemp import EmpresaTempSerializer


class listEmpresaTempViewSet(generics.ListAPIView):
    queryset = EmpresaTemp.objects.all()
    serializer_class = EmpresaTempSerializer

class EmpresaTempViewSet(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class =  EmpresaTempSerializer
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
            return  EmpresaTemp.objects.get(pk=pk)
        except  EmpresaTemp.DoesNotExist:
            raise Http404
    def post(self, request,pk, format=None):
        if request.user.is_superuser:
            serializer =  EmpresaTempSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)      

    def delete(self, request, pk, format=None):
        if 'Authorization' in request.headers.keys():
            token:str = request.headers.get('Authorization')
            token = token.removeprefix('Token ')
            if self.validarCodigoVerificacion(token) & self.validarSuperUser(token) :
                empresaTemp = self.get_object(pk)
                empresaTemp.active = False
                empresaTemp.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)      


urlpatterns = [
    path('empresaTemps/buscar-empresaTemp/<int:pk>/', EmpresaTempViewSet.as_view(), name = " EmpresaTemp"),
    path('empresaTemps/lista-de-empresaTemps', listEmpresaTempViewSet.as_view()),
]
