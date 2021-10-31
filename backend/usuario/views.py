import io
from django.contrib.auth.models import Group, Permission, User
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.admin.models import ACTION_FLAG_CHOICES, LogEntry

import empresa
from .models import Profile
from .serializers import LoginSerializer, ProfileSerializer, UserSerializer, GroupSerializer, PermissionSerializer
from rest_framework import serializers,parsers, renderers,status, permissions, generics, status
from rest_framework.response import Response
from django.http import Http404
from correo.views import RegisterView
from django.contrib.contenttypes.models import ContentType




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
            return Response({'error':'Correo electrónico o contraseña incorrectos.'},status=status.HTTP_400_BAD_REQUEST)
      

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
        response = {
            'groups':serializer_group.data,
            'permissions':serializer_permission.data
        }
        return Response(response)

    def post(self,request):
        if request.user.user_permissions.filter(codename="add_group").exists():
            group = request.data['groups']['name']
            permissions = request.data['permissions']
            newGroup: Group

            if group :
                try :
                    profiles = Profile.objects.filter(empresa=request.user.profile.empresa) 
                    users = User.objects.filter(profile__in=profiles)
                    logs= LogEntry.objects.filter(action_flag=1,content_type_id=3,user__in=users)
                    for log in logs :
                        if Group.objects.filter(pk=log.object_id).exists():
                            groupSeleccionado = Group.objects.get(pk=log.object_id)
                            if groupSeleccionado.name.upper() == group.upper():
                                return Response({'error':'Ya se ha creado un grupo con ese nombre.'},status=status.HTTP_400_BAD_REQUEST)

                    newGroup: Group = Group.objects.create(name=group)
                    for permiso in permissions:
                        if Permission.objects.filter(name=permiso['name']).exists():
                            permiso = Permission.objects.get(name=permiso['name'])
                            newGroup.permissions.add(permiso)

                    content_type = ContentType.objects.get(model='group')
                    log = LogEntry()
                    log.object_id = newGroup.pk
                    log.object_repr = newGroup.name
                    log.action_flag = 1
                    log.change_message = '[{"added": {}}]'
                    log.content_type = content_type
                    log.user = request.user
                    log.save()

                    return Response({'msg':'Se creó con éxito el grupo.'})
                except Exception:
                    newGroup.permissions.clear()
                    newGroup.delete()
                    return Response({'error':'Ocurrió un error al crear el grupo.'})

            return Response({'error':'Debe enviar el nombre de un grupo.'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

    def put(self,request):
        if request.user.user_permissions.filter(codename="change_group").exists():
            if request.data.get('id'):
                if Group.objects.filter(pk=request.data.get('id')):
                    if request.data.get('id') != 3 or request.data.get('id') != 2:
                        group = Group.objects.get(pk=request.data.get('id'))
                        profiles = Profile.objects.filter(empresa=request.user.profile.empresa) 
                        users = User.objects.filter(profile__in=profiles)
                        logs = LogEntry.objects.filter(action_flag=1,content_type_id=3,user__in=users)
                        for log in logs :
                            if Group.objects.filter(pk=log.object_id).exists():
                                grupoSeleccionar = Group.objects.get(pk=log.object_id)
                                if grupoSeleccionar.name.upper() ==  request.data.get('groups').get('name').upper() and grupoSeleccionar.name.upper() != group.name.upper() :
                                    return Response({'error':'Ya se ha creado un grupo con ese nombre.'},status=status.HTTP_400_BAD_REQUEST)
                                    
                        if request.data.get('groups'):
                            group.name = request.data.get('groups').get('name')
                        if request.data.get('permissions'):
                            group.permissions.clear()
                            for permiso in request.data.get('permissions'):
                                if Permission.objects.filter(name=permiso['name']).exists():
                                    permiso = Permission.objects.get(name=permiso['name'])
                                    group.permissions.add(permiso)
                        group.save()
                        return Response({'msg':'Se modificó con éxito el grupo.'})
                    else:
                        return Response({'error':'No tiene permitido modificar esos grupos.'},status=status.HTTP_404_NOT_FOUND)    
                else:
                    return Response({'error':'No se econtró el grupo solicitado.'},status=status.HTTP_404_NOT_FOUND)
                            
            return Response({'error':'Debe enviar el id de un grupo.'},status=status.HTTP_400_BAD_REQUEST)

        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

# views.profile.py

class listProfileViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        admin = request.user
        if admin.user_permissions.filter(codename='view_user').exists():
            profile =ProfileSerializer(Profile.objects.filter(empresa_id = admin.profile.empresa.pk).exclude(pk=admin.profile.pk),many =True)
            profile.data.empresa = ""
            return Response({'profile':profile.data})
        return Response({"error":"No tiene permitido visualizar a los usuarios."},status=status.HTTP_403_FORBIDDEN)    


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
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        if request.user.user_permissions.filter(codename="view_group").exists():
            profiles = Profile.objects.filter(empresa=request.user.profile.empresa) 
            users = User.objects.filter(profile__in=profiles)
            logs= LogEntry.objects.filter(action_flag=1,content_type_id=3,user__in=users)
            grupos:set = set()
            for log in logs :
                if Group.objects.filter(pk=log.object_id).exists():
                    group = Group.objects.get(pk=log.object_id)
                    grupos.add(group)
            grupos.add(Group.objects.get(name='admin_empresa'))
            grupos.add(Group.objects.get(name='cliente'))
            serializer = GroupSerializer(grupos,many=True)
            return Response(serializer.data)
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

class PermisosViewSet(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermissionSerializer

    def get(self,request,pk):
        if request.user.user_permissions.filter(codename="view_permission").exists():
            if Group.objects.filter(pk=pk).exists():
                group = Group.objects.get(pk=pk)
                permissions = PermissionSerializer(group.permissions.all(),many=True)
                return Response({'permissions':permissions.data},status=status.HTTP_200_OK)
            return Response({'error':'No existe el grupo solicitado'},status=status.HTTP_404_NOT_FOUND)    
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

# Permisos grupos del usuario requerido
class PermisosGruposViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        admin= request.user
        serializer:serializers.Serializer
        user_serializer: UserSerializer
        data = None
        if 'application/json' in request.META['CONTENT_TYPE']:
            j_data = request.body
            stream = io.BytesIO(j_data)
            data = parsers.JSONParser().parse(stream)
            
        else:
            data = request.data

        if (not data.get('user').get('id') ) and admin.user_permissions.filter(codename='add_user').exists():
            # if not admin.user_permissions.filter(codename='view_group').exists():
            #     data['user']['groups'] = []
            if not admin.user_permissions.filter(codename='view_permission').exists():
                data['user']['groups'] = []
                # data['user']['permissions'] = []

            serializer = ProfileSerializer(data=data)
            user_serializer = UserSerializer(data=data['user'])
            if serializer.is_valid(raise_exception=True) and user_serializer.is_valid(raise_exception=True):
                profile:Profile
                profile = serializer.save()
                user, newPassword = user_serializer.save()
                profile.empresa = admin.profile.empresa
                profile.user = user
                profile.save()

                try:
                    if newPassword:
                        RegisterView.send_mail(user.email,{'name':user.first_name,'email':user.email,'password':newPassword},"Creación de cuenta de usuario","create_account.html")
                        return Response({'msg':'Usuario creado con éxito'},status=status.HTTP_201_CREATED)
                    else:
                        RegisterView.send_mail(profile.user.email,{'name':profile.user.first_name,'email':profile.user.email},"Creación de cuenta de usuario","create_account.html")
                        return Response({'msg':'Se han actualizado sus datos'},status=status.HTTP_201_CREATED)

                except Exception:
                    if profile.user is not None:
                        profile.user.delete()
                    profile.delete()
                    return Response({"error":"Error al crear usuario"},status=status.HTTP_400_BAD_REQUEST)                    

        elif admin.user_permissions.filter(codename='change_user').exists():
            # if not admin.user_permissions.filter(codename='view_group').exists():
            #     data['user']['groups'] = []
            if not admin.user_permissions.filter(codename='view_permission').exists():
                data['user']['groups'] = []
                # data['user']['permissions'] = []

            if User.objects.filter(pk=data['user']['id']).exists() :
                user = User.objects.get(pk=data['user']['id'])
                user_serializer = UserSerializer(user,data=data['user'])
                data.pop("user")
                profile_serializer = ProfileSerializer(user.profile,data=data)

                if profile_serializer.is_valid(raise_exception=True) and user_serializer.is_valid(raise_exception=True):
                    user_serializer.save()
                    profile_serializer.save()
                    return Response({'msg':"Éxito al actualizar información del usuario."})

            else:
                raise Response({"error": "El usuario no existe"},status=status.HTTP_404_NOT_FOUND)

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
            return Response({"error":"Su usuario no existe en el sistema"},status=status.HTTP_404_NOT_FOUND)

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
                if request.data.get('actual_password'):
                    if not user.check_password(request.data.get('actual_password')):
                        return Response({"error":"Contraseña actual invalida"},status=status.HTTP_400_BAD_REQUEST)        
                user.set_password(request.data.get('password'))
                user.save()
                RegisterView.send_mail(user.email,{'nombre':user.first_name},"Cambio de contraseña","change_password.html")
                return Response({"msg":"Se cambió con exito su contraseña"},status=status.HTTP_200_OK)
            else:
                return Response({"error":"Por favor envie una contraseña valida"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Unauthorized"},status=status.HTTP_403_FORBIDDEN)


class isLogged(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self,request):
        if request.user.is_anonymous:
            return Response({'logged':False})
        return Response({'logged':True})

class ProfileUserViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get(self,request):
        user = request.user
        if user.user_permissions.filter(codename='view_profile').exists():
            serializer = ProfileSerializer(user.profile)
            return Response({'profile':serializer.data})
        return Response({'error':'No tiene permitido ver la información de perfil.'},status=status.HTTP_403_FORBIDDEN)

    def post(self,request):
        data = None
        if 'application/json' in request.META['CONTENT_TYPE']:
            j_data = request.body
            stream = io.BytesIO(j_data)
            data = parsers.JSONParser().parse(stream)
        else:
            data = request.data
        user = request.user
        if user.user_permissions.filter(codename='change_profile'):
            user_serializer = UserSerializer(user,data=data['user'])
            data.pop('user')
            profile_serializer = ProfileSerializer(user.profile,data=data)
            if profile_serializer.is_valid(raise_exception=True):
                if user_serializer.is_valid(raise_exception=True):
                    profile_serializer.save()
                    user_serializer.save()
                    return Response({"msg":"Éxito al actualizar sus datos."})

        return Response({'error':'No tiene permitido cambiar la información de perfil.'},status=status.HTTP_403_FORBIDDEN)
        
