from correo.views import RegisterView
import io
from django.http.request import QueryDict
from django.views.decorators.csrf import csrf_exempt
from usuario.serializers import ProfileSerializer, UserSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from usuario.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from .models import EmpresaTemp, Plan,Empresa
from .serializers import EmpresaTempSerializer, planSerializer,EmpresaSerializer
from rest_framework import parsers, serializers, permissions, generics, status, renderers
from rest_framework.authentication import BaseAuthentication, SessionAuthentication, TokenAuthentication

class planViewSet(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = planSerializer

class listEmpresaViewSet(generics.ListAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class empresaViewSet(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = EmpresaSerializer
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
        serializer = EmpresaSerializer(profile.empresa)
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
                serializer = EmpresaSerializer(empresa, data=request.data)
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


# createEmpresa.py - Registrar solicitud
class CreateView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class= ProfileSerializer
    
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
        serializer: ProfileSerializer 
        profile = None
        token = ""
        if 'application/json' in request.META['CONTENT_TYPE']:
            j_data = request.body
            stream = io.BytesIO(j_data)
            q_data = parsers.JSONParser().parse(stream)
            serializer = ProfileSerializer(data=q_data)

            token = q_data['user']['token']
        else:
            serializer = ProfileSerializer(data=request.data)
            token = request.data['user']['token']

        if self.validarCodigoVerificacion(token) :
            if serializer.is_valid(raise_exception=True):
                profile = serializer.save()
                self.eliminarSolicitud(token)
                return Response({'msg':"Su cuenta se ha creado con éxito"})
        else:
            raise serializers.ValidationError('Ingrese un código de verificación valido')

# views.empresaTemp.py
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
