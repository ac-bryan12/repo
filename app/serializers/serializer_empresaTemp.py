from app.models.empresaTemp import EmpresaTemp
from app.models.empresa import Empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import query
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class EmpresaTempSerializer(serializers.ModelSerializer):
    razonSocial =  serializers.CharField(min_length=5,max_length=50)
    # direccion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=13,min_length=13)
    correo =  serializers.EmailField(min_length=7,required=False)

    class Meta:
        model = Empresa
        fields = ['razonSocial','telefono','correo']

    def validate(self, attrs):
        msg:any
        if len(attrs['razonSocial']) < 5 or len(attrs['razonSocial']) > 50:
            msg = _("Razón Social")
        elif len(attrs['correo']) < 7 :
            msg = _("Email inválido")
        elif EmpresaTemp.objects.filter(correo=attrs['correo']).exists() :
            msg = _("el email ingresado ya existe en el sistema")
        elif len(attrs['telefono']) != 13 :
            msg = _("Teléfono inválido")
        else :
            return attrs
        raise serializers.ValidationError(msg)
        

    def create(self,validated_data):
        print("crear empresa temporal")
        # empresaAttrs = validated_data.pop('organizacion')
        empresa:Empresa = EmpresaTemp()
        empresa.razonSocial = validated_data['razonSocial']
        # empresa.direccion = validated_data['direccion']
        empresa.telefono = validated_data['telefono']
        empresa.correo = validated_data['correo']
        empresa.save()
        return empresa 
    
    
