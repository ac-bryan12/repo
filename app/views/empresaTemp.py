import re
from rest_framework.views import APIView
from app.views.correo import RegisterView
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from app.models.empresaTemp import  EmpresaTemp
from rest_framework import  permissions, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import Http404
from django.urls import path
from app.serializers.serializer_empresaTemp import EmpresaTempSerializer
from rest_framework.authentication import TokenAuthentication

class listEmpresaTempViewSet(generics.ListAPIView):
    queryset = EmpresaTemp.objects.all()
    serializer_class = EmpresaTempSerializer

class EmpresaTempViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
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
    
    def post(self, request):
            try:
                empr = EmpresaTemp.objects.get(correo=request.data['correo'])
                print(empr)
                print(empr.token)
                RegisterView.send_mail(empr.correo,empr.razonSocial,empr.token)
                return Response(status=status.HTTP_201_CREATED)
            except EmpresaTemp.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND) 


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
    path('empresaTemps/buscar-empresaTemp/', EmpresaTempViewSet.as_view(), name = " EmpresaTemp"),
    path('empresaTemps/lista-de-empresaTemps', listEmpresaTempViewSet.as_view()),
]
