import io
from django.contrib.auth.models import Group, Permission, User
from django.db.models.query import QuerySet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.admin.models import  LogEntry

from api.views import PaginationAPIView
from .models import Profile
from .serializers import LoginSerializer, ProfileSerializer, UserSerializer, GroupSerializer, PermissionSerializer
from rest_framework import serializers,parsers, renderers,status, permissions, generics, status
from rest_framework.response import Response
from django.http import Http404
from correo.views import RegisterView
from django.contrib.contenttypes.models import ContentType




class LoginView(APIView):
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
                    user_S = UserSerializer(user)
                    return Response({"token":token.key})
                else:
                    token.delete()
                    token = Token.objects.create(user=user)
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
        group = request.user.groups.get()
        serializer_group = self.serializer_class(group)
        serializer_permission = PermissionSerializer(request.user.groups.get().permissions.all(),many=True)
        response = {
            'groups':serializer_group.data,
            'permissions':serializer_permission.data
        }
        return Response(response)

    # Crea un grupo
    def post(self,request):
        if request.user.has_perm("auth.add_group"):
            group_name = request.data.get('groups')[0]
            permissions = request.data.get('permissions')
            newGroup: Group

            if group_name.get('name') and permissions:
                group_name = group_name.get('name')
                logs = LogEntry.objects.filter(user__profile__empresa=request.user.profile.empresa,action_flag=1,content_type_id=3)
                
                for log in logs:
                    if Group.objects.filter(pk=log.object_id).exists():
                        groupSeleccionado = Group.objects.get(pk=log.object_id)
                        if groupSeleccionado.name.upper() == group_name.upper():
                            return Response({'error':'Ya se ha creado un grupo con ese nombre.'},status=status.HTTP_400_BAD_REQUEST)

                if group_name.lower() == "admin_empresa" or group_name.lower() == "cliente" or group_name.lower() == "default" or group_name.lower() == "admin_facturacion":
                    return Response({'error':'Ya se ha creado un grupo con ese nombre.'},status=status.HTTP_400_BAD_REQUEST)

                newGroup: Group = Group()
                newGroup.name = group_name 
                
                #
                permission_serializer = PermissionSerializer(data=request.data.get('permissions'),many=True)
                if permission_serializer.is_valid(raise_exception=True):
                    newGroup.save()
                    for permiso in permission_serializer.validated_data:
                        permiso = Permission.objects.get(codename=permiso['codename'])
                        newGroup.permissions.add(permiso)
                                
                    
                    if newGroup.permissions.all().filter(codename__in=["view_group","change_group","add_group","add_user","change_user","view_user"]):
                        newGroup.permissions.add(Permission.objects.get(codename="view_permission"))
                                
                    newGroup.permissions.add(Permission.objects.get(codename="view_profile"))
                    newGroup.permissions.add(Permission.objects.get(codename="change_profile"))
                    newGroup.save()
                    #

                    content_type = ContentType.objects.get(model='group')
                    LogEntry.objects.create(object_id = newGroup.pk, object_repr = newGroup.name, action_flag = 1, change_message = '[{"added": {}}]', content_type = content_type, user = request.user)
                    
                    return Response({'msg':'Se creó con éxito el grupo.'})

            return Response({'error':'Debe enviar el nombre de un grupo y sus permisos.'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

    # Actualiza un grupo
    def put(self,request,pk):

        if request.user.has_perm("auth.change_group"):
            
            if Group.objects.filter(pk=pk).exists():
                
                if not pk in [1,2,3,4] :
                    group = Group.objects.get(pk=pk)
                    logs = LogEntry.objects.filter(action_flag=1,content_type_id=3,user__profile__empresa=request.user.profile.empresa)
                    
                    if not logs.filter(object_id=group.pk).exists():
                        return Response({'error':'No existe el grupo indicado.'},status=status.HTTP_404_NOT_FOUND)
                    
                    attrChanged = []
                    
                    if request.data.get('groups'):
        
                        if request.data.get('groups')[0].get('name'):
                            group_name = request.data.get('groups')[0].get('name')
                            
                            for log in logs :
                                if Group.objects.filter(pk=log.object_id).exists():
                                    grupoSeleccionar = Group.objects.get(pk=log.object_id)
                                    if grupoSeleccionar.name.upper() ==  group_name.upper() and grupoSeleccionar.pk != group.pk :
                                        return Response({'error':'Ya se ha creado un grupo con ese nombre.'},status=status.HTTP_400_BAD_REQUEST)
                                    
                            if group_name.lower() == "admin_empresa" or group_name.lower() == "cliente" or group_name.lower() == "default" or group_name.lower() == "admin_facturacion":
                                return Response({'error':'Ya se ha creado un grupo con ese nombre.'},status=status.HTTP_400_BAD_REQUEST)
                        
                            group.name = group_name
                            attrChanged.append("Name")

                    if request.data.get('permissions'):
                        permission_serializer = PermissionSerializer(data=request.data.get('permissions'),many=True)
                        if permission_serializer.is_valid(raise_exception=True):
                            group.permissions.clear()
                            
                            for permiso in permission_serializer.validated_data:
                                permiso = Permission.objects.get(codename=permiso['codename'])
                                group.permissions.add(permiso)
                                    
                            if Permission.objects.get(codename="add_user") in group.permissions.all() or Permission.objects.get(codename="change_user") in group.permissions.all() :
                                group.permissions.add(Permission.objects.get(codename="view_permission"))
                                    
                            group.permissions.add(Permission.objects.get(codename="view_profile"))
                            attrChanged.append("Permissions")
                        
                    group.save()
                    
                    content_type = ContentType.objects.get(model='group')
                    LogEntry.objects.create(object_id = group.pk, object_repr = group.name, action_flag = 2, change_message = '[{"changed": {"fields":'+str(attrChanged)+'}}]', content_type = content_type, user = request.user)
                    
                         
                    return Response({'msg':'Se modificó con éxito el grupo.'})
                
                return Response({'error':'No tiene permitido modificar este grupos.'},status=status.HTTP_403_FORBIDDEN)    
            
            return Response({'error':'No se econtró el grupo solicitado.'},status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

    # borra un grupo
    def delete(self,request,pk):
        if request.user.has_perm('auth.delete_group'):        
            logs = LogEntry.objects.filter(object_id=pk,action_flag=1,content_type_id=3,user__profile__empresa=request.user.profile.empresa)
            
            if logs.exists():
                
                if Group.objects.filter(pk=pk).exists():
                    group: Group = Group.objects.get(pk=pk)
                    users = group.user_set.all()
                    
                    for user in users:
                        user.groups.clear()
                        user.groups.add(Group.objects.get(pk=4))
                        user.save()
                        
                    contentType = ContentType.objects.get(model='group')
                    LogEntry.objects.create(object_id=pk,object_repr=group.name,action_flag=3,change_message='[{"deleted": {}}]',content_type=contentType,user=request.user)
                    
                    group.delete()
                    
                    return Response({'msg':'Se eliminó con éxito el grupo.'})
                  
            return Response({'error':'No se econtró el grupo solicitado.'},status=status.HTTP_404_NOT_FOUND)
        
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)
            

# views.profile.py

class listProfileViewSet(PaginationAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]

    def get(self,request):
        admin = request.user
        if admin.has_perm('auth.view_user'):
            query = Profile.objects.filter(empresa_id = admin.profile.empresa.pk,user__is_active=True).exclude(pk=admin.profile.pk).order_by('-user_id')
            page = self.paginate_queryset(query)
            if page is not None:
                serializer = self.get_paginated_response(ProfileSerializer(page,many=True).data)    
                # profile.data.empresa = ""
                return Response(serializer.data)
            return Response({"error":"Ocurrió un error conla consulta."},status=status.HTTP_400_BAD_REQUEST)
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


# class listUserViewSet(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

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

# envia los grupos de la empresa
class GroupsListPagination(PaginationAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        if request.user.has_perm("auth.view_group"):
            logs= LogEntry.objects.filter(action_flag=1,content_type_id=3,user__profile__empresa=request.user.profile.empresa)
            groups_ids = []
            for log in logs :
                groups_ids.append(log.object_id)
            groups_ids.append('2')
            groups_ids.append('3')
            query = Group.objects.filter(pk__in=groups_ids).order_by('-id')
            page = self.paginate_queryset(query)
            if page is not None:
                serializer = self.get_paginated_response(GroupSerializer(page,many=True).data)
                return Response(serializer.data)
            return Response({"error":"Ocurrió un error con la consulta."},status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)


class GroupsList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        if request.user.has_perm("auth.view_group"):
            logs= LogEntry.objects.filter(action_flag=1,content_type_id=3,user__profile__empresa=request.user.profile.empresa)
            groups_ids = []
            for log in logs :
                groups_ids.append(log.object_id)
            groups_ids.append('2')
            groups_ids.append('3')
            query = Group.objects.filter(pk__in=groups_ids).order_by('-id')
            serializer = GroupSerializer(query,many=True)
            return Response(serializer.data)
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

# envia los permisos de un grupo especificado
class PermisosViewSet(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PermissionSerializer

    def get(self,request,pk):
        
        if request.user.has_perm("auth.view_permission"):
            logs = LogEntry.objects.filter(action_flag=1,content_type_id=3,user__profile__empresa=request.user.profile.empresa,object_id=pk).exists()
            
            if logs and Group.objects.filter(pk=pk).exists() or pk in [2,3]:
                group = Group.objects.get(pk=pk)
                permissions = PermissionSerializer(group.permissions.all().exclude(codename__in=["view_profile","change_profile","view_permission"]),many=True)
                return Response({'permissions':permissions.data},status=status.HTTP_200_OK)
            
            return Response({'error':'No existe el grupo solicitado'},status=status.HTTP_404_NOT_FOUND)    
        
        return Response({'error':'Acceso denegado'},status=status.HTTP_403_FORBIDDEN)

# Permisos y grupos del usuario requerido
class PermisosGruposViewSet(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        admin = request.user
        if admin.has_perm('auth.view_user'):
            empresa = admin.profile.empresa
            user = User.objects.filter(pk=pk)
            if user.exists():
                user = User.objects.get(pk=pk)
                if user.profile.empresa == empresa:
                    group = GroupSerializer(user.groups.get())
                    permissions = PermissionSerializer(user.groups.get().permissions.all().exclude(codename__in=["view_profile","change_profile","view_permission"]),many=True)
                    return Response({"groups":group.data,"permissions":permissions.data},status=status.HTTP_200_OK)
                else:
                    return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)    
            else:
                return Response({"error":"Usuario no existe"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)  

    # creacion de un usuario
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

        if admin.has_perm('auth.add_user') and admin.has_perm('auth.view_permission'):
 
            serializer = ProfileSerializer(data=data)
            user_serializer = UserSerializer(data=data['user'])
            
            if serializer.is_valid(raise_exception=True) and user_serializer.is_valid(raise_exception=True):
                group_id = data['user']['groups'][0]['id']
                logs = LogEntry.objects.filter(action_flag=1,content_type_id=3,user__profile__empresa=request.user.profile.empresa,object_id=group_id).exists()
                
                if logs and Group.objects.filter(pk=group_id).exists() or group_id in ['2','3']:
                    
                    profile:Profile
                    profile = serializer.save()
                    user, newPassword = user_serializer.save()
                    profile.empresa = admin.profile.empresa
                    profile.user = user
                    profile.save()

                    try:
                        
                        RegisterView.send_mail(user.email,{'name':user.first_name,'email':user.email,'password':newPassword},"Creación de cuenta de usuario","create_account.html")
                        
                        contentType = ContentType.objects.get(model='user')
                        LogEntry.objects.create(object_id=profile.user.pk,object_repr=profile.user.email,action_flag=1,change_message='[{"added": {}}]',content_type=contentType,user=request.user)
                        
                        return Response({'msg':'Usuario creado con éxito'},status=status.HTTP_201_CREATED)
                        
                    except Exception:
                        if profile.user is not None:
                            profile.user.delete()
                        profile.delete()
                        return Response({"error":"Error al crear usuario"},status=status.HTTP_400_BAD_REQUEST)
                    
                return Response({"error":"No existe el grupo indicado."},status=status.HTTP_404_NOT_FOUND)
                
                                    
 
    # actualizar un usuario
    def put(self,request,pk):
            
        if request.user.has_perm('auth.change_user'):
            user_serializer: UserSerializer
            data = None
            if 'application/json' in request.META['CONTENT_TYPE']:
                j_data = request.body
                stream = io.BytesIO(j_data)
                data = parsers.JSONParser().parse(stream)
            else:
                data = request.data
            
            if User.objects.filter(pk=pk).exists():
                user = User.objects.get(pk=pk)
                user_serializer = UserSerializer(user,data=data['user'])
                userEntry = data.pop("user")
                profile_serializer = ProfileSerializer(user.profile,data=data)

                if profile_serializer.is_valid(raise_exception=True) and user_serializer.is_valid(raise_exception=True):
                    attrsChanged = []
                    if userEntry.get('groups'):
                        
                        if userEntry.get('groups')[0].get('id'):        
                            group_id = userEntry.get('groups')[0].get('id')
                            logs = LogEntry.objects.filter(action_flag=1,content_type_id=3,user__profile__empresa=request.user.profile.empresa,object_id=group_id).exists()
                
                            if logs :
                                if not Group.objects.filter(pk=group_id).exists():
                                    return Response({"error":"No existe el grupo indicado."},status=status.HTTP_404_NOT_FOUND)
                            elif not group_id in ['2','3'] :
                                return Response({"error":"No existe el grupo indicado."},status=status.HTTP_404_NOT_FOUND)

                            attrsChanged = ["Groups","Permissions"]
                                
                    
                    usuario = user_serializer.save()
                    profile = profile_serializer.save()
                    profile.user = usuario
                    profile.empresa = request.user.profile.empresa
                    profile.save()
                    
                    contentType = ContentType.objects.get(model='user')
                    LogEntry.objects.create(object_id=usuario.pk,object_repr=usuario.email,action_flag=2,change_message='[{"changed": {"fields":'+str(attrsChanged)+'}}]',content_type=contentType,user=request.user)
                    
                    return Response({'msg':"Éxito al actualizar información del usuario."})

            else:
                raise Response({"error": "El usuario no existe"},status=status.HTTP_404_NOT_FOUND)

        return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)


    def delete(self,request,pk):
        if request.user.has_perm("auth.delete_user"):
            logs = LogEntry.objects.filter(action_flag=1,content_type=4,object_id=pk,user__profile__empresa=request.user.profile.empresa).exists()
            
            if logs and User.objects.filter(pk=pk,is_active=True).exists():
                user: User = User.objects.get(pk=pk)
                user.is_active = False
                user.save()
                
                contentType = ContentType.objects.get(model='user')
                LogEntry.objects.create(object_id=user.pk,object_repr=user.email,action_flag=3,change_message='[{"deleted": {}}]',content_type=contentType,user=request.user)
                
                return Response({"msg":"Se eliminó el usuario."})
            
            return Response({"error":"No existe el usuario."},status=status.HTTP_404_NOT_FOUND)
                
        return Response({"error":"Acceso denegado."})

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
                return Response({"msg":"Se cambió con éxito su contraseña"},status=status.HTTP_200_OK)
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


# envia la información de perfil del usuario que la solicita
class ProfileUserViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def get(self,request):
        user = request.user
        if user.has_perm('usuario.view_profile'):
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
        if user.has_perm('usuario.change_profile'):
            user_serializer = UserSerializer(user,data=data['user'])
            data.pop('user')
            profile_serializer = ProfileSerializer(user.profile,data=data)
            if profile_serializer.is_valid(raise_exception=True):
                if user_serializer.is_valid(raise_exception=True):
                    profile_serializer.save()
                    user_serializer.save()
                    return Response({"msg":"Éxito al actualizar sus datos."})

        return Response({'error':'No tiene permitido cambiar la información de perfil.'},status=status.HTTP_403_FORBIDDEN)
        