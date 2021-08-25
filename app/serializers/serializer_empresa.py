from app.models.empresa import Empresa
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import query
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class EmpresaSerializer(serializers.ModelSerializer):
    ruc = serializers.IntegerField()
    razonSocial =  serializers.CharField(max_length=50)
    direccion = serializers.CharField(max_length=30)
    telefono = serializers.IntegerField()
    email =  serializers.EmailField(max_length=250,required=False)

    class Meta:
        model = Empresa
        fields = ['ruc', 'razonSocial','direccion','telefono','email']

    # def validate(self, attrs):
    #     print("validate empresa")
    #     empresa = Empresa.objects.filter(ruc=attrs['ruc'])
    #     print(len(empresa))
    #     if len(empresa)!= 0:
    #         return empresa
    #     msg = _("Empresa no existe en el sistema")
    #     raise serializers.ValidationError(msg)
        

    # def create(self,validated_data):
    #     print("crear empresa")
    #     # empresaAttrs = validated_data.pop('organizacion')
    #     empresa:Empresa = Empresa.objects.get(ruc=validated_data['ruc'])
    #     empresa.razonSocial = validated_data['razonSocial']
    #     empresa.direccion = validated_data['direccion']
    #     empresa.telefono = validated_data['telefono']
    #     empresa.save()
    #     return empresa 
    
