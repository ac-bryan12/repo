from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,Group,Permission

from usuario.validators import validar_identificacion
from .models import Profile
from empresa.serializers import EmpresaSerializer
from rest_framework import serializers, status
from django.utils.translation import gettext_lazy as _
from .models import RUC,CEDULA

# class ProfileViewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['user','empresa']

class GroupSerializer(serializers.ModelSerializer):
    name = serializers.RegexField("^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9_.\-]+$",required=False,max_length=150)
    id  = serializers.CharField(required=False)
    
    class Meta:
        model = Group
        fields = ['name','id']

class PermissionSerializer(serializers.ModelSerializer):
    codename = serializers.RegexField("^[a-zA-Z_]+$",max_length=100,required=False)
    name = serializers.CharField(max_length=255,required=False)
    
    class Meta:
        model=Permission
        fields = ['codename','name']

    def validate(self, attrs):
                    
        if attrs.get('codename'):
            
            if not Permission.objects.filter(codename=attrs.get('codename')).exists():
                raise ValidationError({attrs.get('codename'):"Permiso no encontrado."})
            
            if attrs.get('codename').endswith("empresatemp"):
                raise ValidationError({attrs.get('codename'):"Permiso no encontrado."})
            
        return attrs

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False,allow_blank=True)
    password = serializers.RegexField('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[_.{}=<>;:,\+$@$!%*?&])[A-Za-z\d_.{}=<>;:,\+$@$!%*?&].{7,}',min_length=8,max_length=60,write_only=True,allow_blank=True,required=False)
    username = serializers.CharField(max_length=150,required=False)
    first_name = serializers.RegexField("^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$",min_length=3,max_length=150,required=False)
    last_name = serializers.RegexField("^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$",min_length=3,max_length=150,required=False)
    email = serializers.EmailField(min_length=7,max_length=250,required=False)
    groups = GroupSerializer(required=False,many=True)
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email', 'password','groups']

    def validate(self, attrs):
        if self.instance :
            if User.objects.filter(email=attrs['email']).exclude(email=self.instance.email).exists() :
                raise ValidationError({"error":"El email ingresado ya existe en el sistema"})
            
            if attrs.get('groups'):
                if attrs.get('groups')[0].get('id') == '1':
                    raise ValidationError({"error":"No puede asignar el grupo indicado."})
            
        else: 
            if not attrs.get('first_name'):
                raise ValidationError({"error":"El campo 'first_name' es obligatorio en la creación de usuarios."})
            
            if not attrs.get('last_name'):
                raise ValidationError({"error":"El campo 'last_name' es obligatorio en la creación de usuarios."})
            
            if not attrs.get('groups'):
                raise ValidationError({"error":"El campo 'groups' es obligatorio en la creación de usuarios."})
            
            elif not attrs.get('groups')[0].get('id'):
                raise ValidationError({"error":"El campo 'groups.id' es obligatorio en la creación de usuarios."})
            
            elif not Group.objects.filter(pk=attrs.get('groups')[0].get('id')).exists():
                raise ValidationError({"error":"No existe el grupo indicado."})
            
            elif attrs.get('groups')[0].get('id') == '1' :
                raise ValidationError({"error":"No puede asignar el grupo indicado."})

            if not attrs.get('email'):
                raise ValidationError({"error":"El campo 'email' es obligatorio en la creación de usuarios."})
            elif User.objects.filter(email=attrs['email']).exists() :
                raise ValidationError({"error":"El email ingresado ya existe en el sistema"})
                
        return attrs

    def create(self,validated_data):
        user:User = User()    
        user.set_unusable_password()
        user.username = validated_data['email']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        newPassword = None
        if validated_data.get("password"):
            if validated_data.get("password") != "":
                user.set_password(validated_data['password'])

        elif not user.has_usable_password():
            allow_chars = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789_.=<>;:,$%*?&"
            newPassword = BaseUserManager.make_random_password(self,length=16,allowed_chars=allow_chars)
            user.set_password(newPassword)
        else:
            newPassword = None
        user.save()
        if validated_data.get('groups'):
            user.groups.add(Group.objects.get(pk=validated_data['groups'][0].get('id')))

        user.save()
        return user,newPassword

    def update(self, instance, validated_data):
        if validated_data.get('first_name'):
            instance.first_name = validated_data['first_name']
        if validated_data.get('last_name'):
            instance.last_name = validated_data['last_name']
        if validated_data.get('email'):
            instance.email = validated_data['email']
            instance.username = validated_data['email']

        if validated_data.get('groups'):
            if validated_data.get('groups')[0].get('id'):
                instance.groups.clear()
                instance.groups.add(Group.objects.get(pk=validated_data['groups'][0]['id']))

        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    n_identificacion = serializers.CharField(max_length=13)
    tipo_identificacion = serializers.ChoiceField(choices=[RUC,CEDULA])
    user = UserSerializer(required=False)
    empresa = EmpresaSerializer(required=False,write_only=True)
    direccion = serializers.RegexField("^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9._ ]+$",max_length=150,required=False)
    telefono =  serializers.RegexField("^[0-9]+$",max_length=13,required=False)
    cargoEmpres = serializers.RegexField("^[a-zA-ZñÑáéíóúÁÉÍÓÚ ]+$",max_length=150,required=False)
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
        else:
            if Profile.objects.filter(pk = attrs["n_identificacion"]).exists() and attrs['n_identificacion'] != self.instance.n_identificacion:
                raise ValidationError({"error":"El número de identificación ingresado ya existe en el sistema."})
        return attrs
    
    def validate_n_identificacion(self,value):
        return validar_identificacion(value)

    def update(self, instance, validated_data):
        instance.delete()
        profile: Profile = Profile()
        profile.pk = validated_data['n_identificacion']
        profile.tipo_identificacion = validated_data['tipo_identificacion']
        profile.telefono = validated_data['telefono']
        profile.direccion = validated_data['direccion']
        if validated_data.get("cargoEmpres"):
            profile.cargoEmpres = validated_data['cargoEmpres']
        profile.save()
        return profile
        
            
        

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=60,write_only=True)

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