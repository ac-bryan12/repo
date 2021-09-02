from app.models.empresa import Empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import query
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class EmpresaSerializer(serializers.ModelSerializer):
    ruc = serializers.CharField(min_length=13,max_length=13)
    razonSocial =  serializers.CharField(min_length=5,max_length=50)
    direccion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=10,min_length=10)
    email =  serializers.EmailField(min_length=7,required=False)

    class Meta:
        model = Empresa
        fields = ['ruc', 'razonSocial','direccion','telefono','email']

    def validate(self, attrs):
        msg:any
        if len(attrs['ruc']) != 13 :
            msg = _("Ruc inválido")
        elif Empresa.objects.filter(ruc=attrs['ruc']).exists() :
            msg = _("El Ruc ingresado ya existe en el sistema")
        elif len(attrs['razonSocial']) < 5 or len(attrs['razonSocial']) > 50:
            msg = _("Razón Social")
        elif len(attrs['email']) < 7 :
            msg = _("Email inválido")
        elif Empresa.objects.filter(correo=attrs['email']).exists() :
            msg = _("el email ingresado ya existe en el sistema")
        elif len(attrs['telefono']) != 10 :
            msg = _("Teléfono inválido")
        else :
            return attrs
        raise serializers.ValidationError(msg)
        

    # def create(self,validated_data):
    #     print("crear empresa")
    #     # empresaAttrs = validated_data.pop('organizacion')
    #     empresa:Empresa = Empresa.objects.get(ruc=validated_data['ruc'])
    #     empresa.razonSocial = validated_data['razonSocial']
    #     empresa.direccion = validated_data['direccion']
    #     empresa.telefono = validated_data['telefono']
    #     empresa.save()
    #     return empresa 
    
