from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ValidationError
import empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group,Permission
from .models import Profile
from empresa.models import Empresa
from empresa.serializers import EmpresaSerializer
from rest_framework import permissions, serializers
from django.utils.translation import gettext_lazy as _

# class ProfileViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['user','empresa']

class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)

    class Meta:
        model=Group
        fields = ['name']
    
    def to_representation(self, instance):
        return instance.name

class PermissionSerializer(serializers.ModelSerializer):
    codename = serializers.CharField(max_length=100)

    class Meta:
        model=Permission
        fields = ['codename']

    def to_representation(self, instance):
        return instance.codename

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    password = serializers.CharField(min_length=8,write_only=True,allow_blank=True,required=False)
    username = serializers.CharField(max_length=150,required=False)
    first_name = serializers.CharField(min_length=3,max_length=50)
    last_name = serializers.CharField(min_length=3,max_length=50)
    email = serializers.EmailField(min_length=7)
    groups = GroupSerializer(required=False,many=True,write_only=True)
    permissions = PermissionSerializer(required=False,many=True,write_only=True)

    class Meta:
        model = User
        fields = ['id','is_superuser','username','first_name','last_name','email', 'password','groups','permissions']

    def validate(self, attrs):
        if attrs.get("id"):
            if not User.objects.filter(pk = attrs["id"]).exists():
                if attrs.get("password") == "":
                    raise ValidationError({'error':'Debe ingresar una contraseña'})
                return attrs
            return attrs
        else :
            if User.objects.filter(email=attrs['email']).exists() :
                raise ValidationError({"error":"El email ingresado ya existe en el sistema"})
            return attrs

    def create(self,validated_data):
        user:User
        if validated_data.get("id"):
            if User.objects.filter(pk=validated_data['id']).exists() :
                user = User.objects.get(pk=validated_data['id'])
            else:
                raise ValidationError({"error": "El usuario no existe"})
        else:
            user = User()
            user.set_unusable_password()
        print("crear usuario")
        user.username = validated_data['email']
        user.email = validated_data['email']
        print("validar: ",validated_data.get("password"),user.has_usable_password())
        if validated_data.get("password"):
            if validated_data.get("password") != "":
                user.set_password(validated_data['password'])
                print("usable_password:",user.has_usable_password())
                newPassword = validated_data['password']
        elif not user.has_usable_password():
            allow_chars = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789_.=<>;:,$%*?&"
            newPassword = BaseUserManager.make_random_password(self,length=16,allowed_chars=allow_chars)
            print(newPassword)
            user.set_password(newPassword)
        else:
            newPassword = None
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        if validated_data.get('groups'):
            for group in validated_data['groups'] :
                user.groups.add(Group.objects.get(name=group.get('name')))
                if validated_data.get('permissions') :
                    user.user_permissions.clear()
                    for permission in validated_data['permissions'] :
                        user.user_permissions.add(Permission.objects.get(codename=permission.get('codename')))
                else:
                    print(Group.objects.get(name=group.get('name')).permissions.all())
                    user.user_permissions.set(Group.objects.get(name=group.get('name')).permissions.all())
        user.save()
        return user,newPassword

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    empresa = EmpresaSerializer(required=False)
    direccion = serializers.CharField(max_length=150,required=False)
    telefono =  serializers.CharField(max_length=10,min_length=10,required=False)
    cargoEmpres = serializers.CharField(max_length=150,required=False)
    # firmaElectronica = serializers.CharField(max_length=100,required=False) # Ni idea de que va aca

    class Meta:
        model = Profile
        fields = ['user','empresa','direccion','telefono','cargoEmpres'] # 'firmaElectronica'


    def create(self,validated_data):
        empresa_serializer = None
        empresa = None
        if validated_data.get('empresa'):
            empresa_serializer = EmpresaSerializer(data=validated_data.get('empresa'))
            empresa_serializer.is_valid(raise_exception=True)
            empresa = empresa_serializer.save()
        user_serializer = UserSerializer(data=validated_data.get('user'))

        if user_serializer.is_valid():
            user,newPassword = user_serializer.save()
            profile:Profile = user.profile
            profile.direccion = validated_data['direccion']
            profile.telefono = validated_data['telefono']
            profile.cargoEmpres = validated_data['cargoEmpres']
            if empresa:
                profile.empresa = empresa
            profile.save()
            return profile,newPassword
        return None

    # def addPermissions(self,user:User):
    #     user.user_permissions.add(
    #         Permission.objects.get(codename='add_user'),Permission.objects.get(codename='view_user'),Permission.objects.get(codename='delete_user'),Permission.objects.get(codename='change_user'),
    #         Permission.objects.get(codename='add_empresa'),Permission.objects.get(codename='view_empresa'),Permission.objects.get(codename='delete_empresa'),Permission.objects.get(codename='change_empresa'),
    #         Permission.objects.get(codename='view_profile'),Permission.objects.get(codename='change_profile'),
    #         Permission.objects.get(codename='add_group'),Permission.objects.get(codename='view_group'),Permission.objects.get(codename='delete_group'),Permission.objects.get(codename='change_group'),
    #         Permission.objects.get(codename='add_permission'),Permission.objects.get(codename='view_permission'),Permission.objects.get(codename='delete_permission'),Permission.objects.get(codename='change_permission'),
    #     )

# Auth

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30,write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self,attrs):
        user:User
        try:
            userAcount:User = User.objects.get(email=attrs['email'])
            user = authenticate(username=userAcount.username,password=attrs['password'])

            if user is not None :
                attrs['email'] = user
            else:
                # msg = _('User invalid')
                # raise serializers.ValidationError(msg,code='authorization')
                attrs['email'] = None
        except User.DoesNotExist:
            attrs['email'] = None
        return attrs

# class PermissionsListSerializer(serializers.ModelSerializer):
#     codename = serializers.CharField(max_length=100)

#     class Meta:
#         model=Permission
#         fields = ['codename']

#     def to_representation(self, instance):
#         return instance.codename