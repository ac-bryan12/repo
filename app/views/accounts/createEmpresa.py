from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from app.models.empresaTemp import EmpresaTemp
from app.serializers.serializer_profile import ProfileSerializer
from rest_framework import parsers, renderers
from rest_framework.views import APIView
from rest_framework import serializers
from django.http import QueryDict
from django.urls import path
from rest_framework.parsers import JSONParser
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import *
import io
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication


class CreateView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class= ProfileSerializer
    authentication_classes = (BasicAuthentication,)
    
    def eliminarSolicitud(self,token):
        empresa:EmpresaTemp = EmpresaTemp.objects.filter(token=token)
        empresa.delete()

    
    def validarCodigoVerificacion(self,token):
        try:
            if EmpresaTemp.objects.filter(token=token).exists() :
                return True
            else:
                return False
        except:
            return False

    
    @csrf_exempt
    def post(self, request):
        serializer:serializers.Serializer
        profile = None
        q_data:QueryDict
        token = ""
        if 'Authorization' in request.headers.keys():
            token:str = request.headers.get('Authorization')
            token = token.removeprefix('Token ')
            if self.validarCodigoVerificacion(token) :
                # self.eliminarSolicitud(token)

                if 'application/json' in request.META['CONTENT_TYPE']:
                    j_data = request.body
                    stream = io.BytesIO(j_data)
                    q_data = JSONParser().parse(stream)
                    serializer = ProfileSerializer(data=q_data)
                else:
                    serializer = ProfileSerializer(data=request.data)

                if serializer.is_valid(raise_exception=True):
                    profile = serializer.save()
                    self.eliminarSolicitud(token)
                    return Response({'msg':"Su cuenta se ha creado con éxito"})
            else:
                raise serializers.ValidationError('Ingrese un código de verificación valido')



    
        

urlpatterns = [
    path('create/', CreateView.as_view()),
    # path('auth/', ObtainAuthToken.as_view()),
]