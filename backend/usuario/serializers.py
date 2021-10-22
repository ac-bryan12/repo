from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ValidationError
import empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group,Permission
from .models import Profile
from empresa.models import Empresa
from empresa.serializers import EmpresaSerializer
from rest_framework import permissions, serializers, status
from django.utils.translation import gettext_lazy as _
from .models import RUC,CEDULA

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
    id = serializers.CharField(required=False,allow_blank=True)
    password = serializers.CharField(min_length=8,write_only=True,allow_blank=True,required=False)
    username = serializers.CharField(max_length=150,required=False)
    first_name = serializers.CharField(min_length=3,max_length=50)
    last_name = serializers.CharField(min_length=3,max_length=50)
    email = serializers.EmailField(min_length=7)
    groups = GroupSerializer(required=False,many=True)
    permissions = PermissionSerializer(required=False,many=True,write_only=True)

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email', 'password','groups','permissions']

    def validate(self, attrs):
        if self.instance :
            
            if User.objects.filter(email=attrs['email']).exclude(email=self.instance.email).exists() :
                raise ValidationError({"error":"El email ingresado ya existe en el sistema"})
        
        else: 
            
            if User.objects.filter(email=attrs['email']).exists() :
                raise ValidationError({"error":"El email ingresado ya existe en el sistema"})
                
        return attrs

    def create(self,validated_data):
        user:User = User()    
        user.set_unusable_password()
        user.username = validated_data['email']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']

        if validated_data.get("password"):
            if validated_data.get("password") != "":
                user.set_password(validated_data['password'])
                newPassword = None

        elif not user.has_usable_password():
            allow_chars = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789_.=<>;:,$%*?&"
            newPassword = BaseUserManager.make_random_password(self,length=16,allowed_chars=allow_chars)
            user.set_password(newPassword)
        else:
            newPassword = None

        user.save()

        if validated_data.get('groups'):
            for group in validated_data['groups'] :
                user.groups.add(Group.objects.get(name=group.get('name')))

        if validated_data.get('permissions') :
            for permission in validated_data['permissions'] :
                user.user_permissions.add(Permission.objects.get(codename=permission.get('codename')))
        elif validated_data.get('groups'): 
            user.user_permissions.set(Group.objects.get(name=group.get('name')).permissions.all())

        user.save()
        return user,newPassword

    def update(self, instance, validated_data):
        user:User = instance
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.email = validated_data['email']
        user.username = validated_data['email']
        user.save()

        keys = validated_data.keys()
        if 'groups' in keys:
            user.groups.clear()
            user.user_permissions.clear()

        if validated_data.get('groups'):
            for group in validated_data['groups'] :
                user.groups.add(Group.objects.get(name=group.get('name')))

        
        if validated_data.get('permissions'):
            for permission in validated_data['permissions'] :
                user.user_permissions.add(Permission.objects.get(codename=permission.get('codename')))
        else:
            if validated_data.get('groups'):
                user.user_permissions.set(Group.objects.get(name=group.get('name')).permissions.all())

        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    n_identificacion = serializers.CharField(max_length=13)
    tipo_identificacion = serializers.ChoiceField(choices=[RUC,CEDULA])
    user = UserSerializer(required=False)
    empresa = EmpresaSerializer(required=False,write_only=True)
    direccion = serializers.CharField(max_length=150,required=False)
    telefono =  serializers.CharField(max_length=10,min_length=10,required=False)
    cargoEmpres = serializers.CharField(max_length=150,required=False)
    # firmaElectronica = serializers.CharField(max_length=100,required=False) # Ni idea de que va aca

    class Meta:
        model = Profile
        fields = ['n_identificacion','tipo_identificacion','user','empresa','direccion','telefono','cargoEmpres'] # 'firmaElectronica'

    def create(self,validated_data):        
        profile:Profile = Profile()
        profile.n_identificacion = validated_data['n_identificacion']
        profile.tipo_identificacion = validated_data['tipo_identificacion']
        profile.direccion = validated_data['direccion']
        profile.telefono = validated_data['telefono']
        profile.cargoEmpres = validated_data['cargoEmpres']
        return profile

    def validate(self, attrs):
        if not self.instance:
            if Profile.objects.filter(pk = attrs["n_identificacion"]).exists():
                raise ValidationError({"error":"El número de identificación ingresado ya existe en el sistema."})
        return attrs

    def update(self, instance, validated_data):
        profile:Profile = instance
        profile.n_identificacion = validated_data['n_identificacion']
        profile.tipo_identificacion = validated_data['tipo_identificacion']
        profile.telefono = validated_data['telefono']
        profile.direccion = validated_data['direccion']
        if validated_data.get("cargoEmpres"):
            profile.cargoEmpres = validated_data['cargoEmpres']
        profile.save()
        return profile
        
            
        

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