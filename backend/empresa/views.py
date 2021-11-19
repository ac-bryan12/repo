from correo.views import RegisterView
import io
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
from .serializers import  EmpresaTempSerializer, planSerializer,EmpresaSerializer
from rest_framework import parsers, serializers, permissions, generics, status, renderers
from rest_framework.authentication import TokenAuthentication



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

    def get(self, request,format=None):
        if request.user.has_perm("empresa.view_empresa"):
            profile:Profile = request.user.profile
            serializer = EmpresaSerializer(profile.empresa)
            return Response(serializer.data)
        return Response({'error':'No tiene permitido visualizar la información de la empresa.'},status=status.HTTP_403_FORBIDDEN)
  

    def post(self, request):
        if request.user.has_perm("empresa.change_empresa"):
            empresa = request.user.profile.empresa
            serializer = EmpresaSerializer(empresa, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"msg":"Se han actualizado sus datos"},status=status.HTTP_200_OK)
            # else:
            #     print(serializer.errors)
            #     return Response({"error":"Ocurrió un error al intentar actualizar sus datos."}, status=status.HTTP_400_BAD_REQUEST)  
        return Response({'error':'No tiene permitido cambiar la información de la empresa.'},status=status.HTTP_403_FORBIDDEN)


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


# /create-cuenta 
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
        empresa_serializer: EmpresaSerializer
        user_serializer: UserSerializer
        data = None

        if 'application/json' in request.META['CONTENT_TYPE']:
            j_data = request.body
            stream = io.BytesIO(j_data)
            data = parsers.JSONParser().parse(stream)
        else:
            data = request.data

        token =data['token']
        serializer = ProfileSerializer(data=data)
        empresa_serializer = EmpresaSerializer(data=data['empresa'])
        user_serializer = UserSerializer(data=data['user'])
        if self.validarCodigoVerificacion(token) :
            if serializer.is_valid(raise_exception=True) and empresa_serializer.is_valid(raise_exception=True) and user_serializer.is_valid(raise_exception=True):
                profile = serializer.save()
                user, password = user_serializer.save()
                empresa = empresa_serializer.save()
                profile.user = user
                profile.empresa = empresa
                profile.save()
                self.eliminarSolicitud(token)
                RegisterView.send_mail(user.email,{"name":user.first_name,"email":user.email,"password":password},"Creación de Cuenta","create_account.html")
                return Response({'msg':"Su cuenta se ha creado con éxito"})
        else:
            raise serializers.ValidationError({"error":'Ingrese un código de verificación valido'})

# views.empresaTemp.py
class listEmpresaTempViewSet(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    # queryset = EmpresaTemp.objects.all()

    def get(self,request):
        if request.user.has_perm("empresa.view_empresatemp"):
            serializer= EmpresaTempSerializer(EmpresaTemp.objects.all(),many=True)
            return Response(serializer.data)
        return Response({'error':'Acceso denegado.'},status=status.HTTP_403_FORBIDDEN)

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
        if request.user.has_perm("empresa.view_empresatemp"):
            try:
                empr = EmpresaTemp.objects.get(correo=request.data['correo'])
                print(empr)
                print(empr.token)
                RegisterView.send_mail(empr.correo,{'razonSocial':empr.razonSocial,'token':empr.token},"Creación de cuenta","envioCorreo.html")
                return Response(status=status.HTTP_201_CREATED)
            except EmpresaTemp.DoesNotExist: 
                return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response({'error':'Acceso denegado.'},status=status.HTTP_403_FORBIDDEN)


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
