from app.models.profile import Profile
from app.models.empresa import Empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission, User
from django.db.models import query
from rest_framework import serializers
from .serializer_empresa import EmpresaSerializer
from .serializer_user import UserSerializer
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _



class ProfileViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','empresa']


class ProfileSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    empresa = EmpresaSerializer()


    # firmaElectronica = serializers.TextField(max_length=100,null=True) # Ni idea de que va aca

    class Meta:
        model = Profile
        fields = ['usuario','empresa']

    # def validate(self, attrs):
        
    #     empresa = Token.objects.filter(key=attrs['usuario']).exists()
    #     if len(empresa)!= 0:
    #         return attrs
    #     raise serializers.ValidationError("Empresa no existe en el sistema")

    def create(self,validated_data):

        # empresa = EmpresaSerializer(validated_data['empresa'])
        # empresa:Empresa = Empresa.objects.get(ruc=validated_data['empresa']['ruc'])
        empresa:Empresa = Empresa()
        empresa.ruc = validated_data['empresa']['ruc']
        empresa.razonSocial = validated_data['empresa']['razonSocial']
        empresa.direccion = validated_data['empresa']['direccion']
        empresa.telefono = validated_data['empresa']['telefono']
        empresa.correo = validated_data['empresa']['email']
        empresa.save()

        # user = UserSerializer(validated_data['user'])
        user:User = User()
        user.username = validated_data['usuario']['email']
        user.email = validated_data['usuario']['email']
        user.set_password(validated_data['usuario']['password'])
        user.first_name = validated_data['usuario']['firstName']
        user.last_name = validated_data['usuario']['lastName']
        user.save()
        self.addPermissions(user)

        user.groups.add(Group.objects.get(name='admin_empresa'))
        
        profile:Profile = user.profile
        profile.empresa = empresa
        profile.direccion = validated_data['usuario']['direccion']
        profile.telefono = validated_data['usuario']['telefono']
        profile.cargoEmpres = validated_data['usuario']['cargo']
        profile.save()
        return profile

    def addPermissions(self,user:User):
        user.user_permissions.add(
            Permission.objects.get(codename='add_user'),Permission.objects.get(codename='view_user'),Permission.objects.get(codename='delete_user'),Permission.objects.get(codename='change_user'),
            Permission.objects.get(codename='add_empresa'),Permission.objects.get(codename='view_empresa'),Permission.objects.get(codename='delete_empresa'),Permission.objects.get(codename='change_empresa'),
            Permission.objects.get(codename='view_profile'),Permission.objects.get(codename='change_profile'),
            Permission.objects.get(codename='add_group'),Permission.objects.get(codename='view_group'),Permission.objects.get(codename='delete_group'),Permission.objects.get(codename='change_group'),
            Permission.objects.get(codename='add_permission'),Permission.objects.get(codename='view_permission'),Permission.objects.get(codename='delete_permission'),Permission.objects.get(codename='change_permission'),
        )