import datetime
import io
from django.contrib.auth.models import Group, Permission, User
from django.utils import tree
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .models import Profile
from .serializers import LoginSerializer, ProfileSerializer, UserSerializer, GroupSerializer, PermissionSerializer
from rest_framework import serializers,parsers, renderers,status, permissions, generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib.sessions.models import Session
from django.http import Http404
from correo.views import RegisterView




class LoginView(APIView):
    # throttle_classes = ()
    # permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = [permissions.AllowAny]
    serializer_class= LoginSerializer

    def post(self, request):
        serializer:serializers.Serializer
        if 'application/json' in request.META['CONTENT_TYPE']:
            j_data = request.body
            stream = io.BytesIO(j_data)
            q_data = parsers.JSONParser().parse(stream)
            serializer = LoginSerializer(data=q_data)
        else:
            serializer = LoginSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user:User = serializer.validated_data['email']
        if user is not None :
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                if created :
                    # login(request, user)
                    user_S = UserSerializer(user)
                    return Response({"token":token.key})
                else:
                    # Botarlo de la session

                    # all_sessions = Session.objects.filter(expire_date__gte=datetime.now())
                    # if all_sessions.exists():
                    #     for session in all_sessions:
                    #         session_data = session.get_decoded()
                    #         if user.pk == int(session_data.get('_auth_user_id')):
                    #             print('borrado')
                    #             session.delete()
                    token.delete()
                    token = Token.objects.create(user=user)
                    # login(request, user)
                    
                    user_S = UserSerializer(user)
                    return Response({"token":token.key})
                    
        else: 
            return Response({'error':'El usuario no existe en el sistema'},status=status.HTTP_400_BAD_REQUEST)
      

class LogoutView(APIView):

    def post(self, request):
        request.user.auth_token.delete()
        data = {"estado": "SESION_TERMINADA"}
        return Response(data, status=status.HTTP_200_OK)

# Envia los permisos y grupos del usuario que ha iniciado sessión
class UserPermissionView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class= GroupSerializer

    def get(self,request):
        serializer_group = self.serializer_class(request.user.groups.all(),many=True)
        serializer_permission = PermissionSerializer(request.user.user_permissions.all(),many=True)
        response = Response()
        group = JSONRenderer().render(serializer_group.data)
        permissions = JSONRenderer().render(serializer_permission.data)
        response.set_cookie('group',group.decode("utf-8"))
        response.set_cookie('permissions',permissions.decode("utf-8"))
        return response

# views.profile.py

class listProfileViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        admin = request.user
        if admin.user_permissions.filter(codename='view_user').exists():
            profile =ProfileSerializer(Profile.objects.filter(empresa_id = admin.profile.empresa.pk).exclude(pk=admin.profile.pk),many =True)
            return Response({'profile':profile.data})
        return Response({"msg":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)    


class profileViewSet(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ProfileSerializer
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
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request,pk,format=None):
        if 'Authorization' in request.headers.keys():
            token:str = request.headers.get('Authorization')
            token = token.removeprefix('Token ')
            if self.validarCodigoVerificacion(token) & self.validarSuperUser(token) :
                profile = self.get_object(pk)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            else:
                return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)

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
                serializer = ProfileSerializer(empresa, data=request.data)
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
                profile = self.get_object(pk)
                profile.active = False
                profile.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)      


class listUserViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserViewSet(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
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
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request,pk,format=None):
        if 'Authorization' in request.headers.keys():
            token:str = request.headers.get('Authorization')
            token = token.removeprefix('Token ')
            if self.validarCodigoVerificacion(token) & self.validarSuperUser(token) :
                profile = self.get_object(pk)
                serializer = UserSerializer(profile)
                return Response(serializer.data)
            else:
                return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)

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
                serializer = UserSerializer(empresa, data=request.data)
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
                profile = self.get_object(pk)
                profile.active = False
                profile.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED) 
        else:
            return Response("No se ha encontrado su pagina",status = status.HTTP_401_UNAUTHORIZED)      

# views.grupos.py
class GroupViewSet(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermisosViewSet(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        permissions = PermissionSerializer(Group.objects.get(name = "admin_empresa").permissions.all(),many=True)
        return Response({'permissions':permissions.data},status=status.HTTP_200_OK)

# Permisos grupos del usuario requerido
class PermisosGruposViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        admin= request.user
        if admin.user_permissions.filter(codename='change_user').exists() and admin.user_permissions.filter(codename='add_user').exists() and admin.user_permissions.filter(codename='view_group').exists() and admin.user_permissions.filter(codename='view_permission').exists():
            serializer:serializers.Serializer
            if 'application/json' in request.META['CONTENT_TYPE']:
                j_data = request.body
                stream = io.BytesIO(j_data)
                q_data = parsers.JSONParser().parse(stream)
                serializer = ProfileSerializer(data=q_data)
            else:
                serializer = ProfileSerializer(data=request.data)
            
            if serializer.is_valid(raise_exception=True):
                profile = serializer.save()
                profile.empresa = request.user.profile.empresa
                profile.save()
                return Response({'msg':'Usuario creado con éxito'},status=status.HTTP_201_CREATED)
        return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)    

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
                    return Response({"groups":group.data,"permissions":permissions.data},status=status.HTTP_200_OK)
                else:
                    return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)    
            else:
                return Response({"error":"Usuario no existe"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)    

class PasswordResetTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request,email):
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                token.delete()
                token = Token.objects.create(user=user)
            context = {"nombre":user.first_name,"token":token}
            RegisterView.send_mail(email,context,"Restablecimiento de Contraseña","password_reset.html")
            return Response({"msg":"Se le enviará un token a su correo electrónico."},status=status.HTTP_200_OK)
        else:
            return Response({"error":"No existe en el sistema"},status=status.HTTP_404_NOT_FOUND)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request,token):
        if Token.objects.filter(key=token).exists():
            return Response({"msg":"Código correcto","validated":True},status=status.HTTP_200_OK)
        else:
            return Response({"error":"Código incorrecto","validated":False},status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        
        if not request.user.is_anonymous:
            user:User = request.user
            if request.data.get('password'):
                user.set_password(request.data.get('password'))
                user.save()
                return Response({"msg":"Se cambió con exito su contraseña"},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Por favor envie una contraseña valida"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Unauthorized"},status=status.HTTP_403_FORBIDDEN)