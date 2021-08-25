from app.models.empresaTemp import EmpresaTemp
from django.contrib.auth.models import User
from app.models.profile import Profile
from rest_framework.serializers import Serializer
from app.serializers.serializer_profile import ProfileSerializer
from rest_framework import parsers, renderers
from rest_framework.views import APIView
from rest_framework import routers, serializers, viewsets
from django.http import QueryDict
from django.utils.http import urlencode
from rest_framework.response import Response
from django.urls import path, include,re_path
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

import json
import io

class CreateView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class= ProfileSerializer
    
    def eliminarSolicitud(self,token):
        empresa:EmpresaTemp = EmpresaTemp.objects.filter(token=token)
        empresa.delete()

    def post(self, request):
        serializer:serializers.Serializer
        profile = None
        q_data:QueryDict
        token = ""
        if 'Authorization' in request.headers.keys():
            token:str = request.headers.get('Authorization')
            token = token.removeprefix('Token ')
            print(token)
        if EmpresaTemp.objects.filter(token=token).exists() :

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
                return Response({'msg': 'se creó con exito la cuenta'})
        else:
            return Response({'msg':'Ingrese un código de verificación valido'})
        


    
        

urlpatterns = [
    path('create/', CreateView.as_view()),
    # path('auth/', ObtainAuthToken.as_view()),
]