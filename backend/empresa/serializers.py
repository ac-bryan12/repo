from empresa.models import Empresa,EmpresaTemp,Plan
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _




class EmpresaSerializer(serializers.ModelSerializer):
    ruc = serializers.CharField(max_length=13)
    razonSocial =  serializers.CharField(max_length=150)
    direccion = serializers.CharField(max_length=150)
    telefono = serializers.CharField(max_length=13)
    correo =  serializers.EmailField(min_length=7,max_length=150)

    class Meta:
        model = Empresa
        fields = ['ruc', 'razonSocial','direccion','telefono','correo']

    def validate(self, attrs):
        msg:any
        if not self.instance:
            if Empresa.objects.filter(ruc=attrs['ruc']).exists() :
                msg = _("El Ruc ingresado ya existe en el sistema")
            elif Empresa.objects.filter(correo=attrs['correo']).exists() :
                msg = _("El email ingresado ya existe en el sistema")
            else :
                return attrs
        else:
            if Empresa.objects.filter(correo=attrs['correo']).exclude(correo = self.instance.correo).exists() :
                msg = _("El email ingresado ya existe en el sistema")
            else:
                return attrs
        raise serializers.ValidationError(msg)
        

    # def create(self,validated_data):
    #     empresa:Empresa = Empresa()
    #     empresa.ruc = validated_data['ruc']
    #     empresa.razonSocial = validated_data['razonSocial']
    #     empresa.correo = validated_data['correo']
    #     empresa.direccion = validated_data['direccion']
    #     empresa.telefono = validated_data['telefono']
    #     empresa.save()
    #     return empresa 

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.correo = validated_data['correo']
        instance.direccion = validated_data['direccion']
        instance.telefono = validated_data['telefono']
        instance.save()
        return instance

class EmpresaTempSerializer(serializers.ModelSerializer):
    razonSocial =  serializers.CharField(max_length=150)
    telefono = serializers.CharField(max_length=13)
    correo =  serializers.EmailField(min_length=7,max_length=150)
    # direccion = serializers.CharField(max_length=150)
    descripcion = serializers.CharField(max_length=250)
    cargo = serializers.CharField(max_length=150)
    nombre = serializers.CharField(max_length=150)

    class Meta:
        model = Empresa
        fields = ['razonSocial','telefono','correo','direccion','descripcion','cargo','nombre']

    def validate(self, attrs):
        msg:any
        if EmpresaTemp.objects.filter(correo=attrs['correo']).exists() :
            msg = _("el email ingresado ya existe en el sistema")
        else :
            return attrs
        raise serializers.ValidationError(msg)
        

    def create(self,validated_data):
        empresa:EmpresaTemp = EmpresaTemp()
        empresa.razonSocial = validated_data['razonSocial']
        # empresa.direccion = validated_data['direccion']
        empresa.telefono = validated_data['telefono']
        empresa.correo = validated_data['correo']
        empresa.nombre = validated_data['nombre']
        empresa.descripcion = validated_data['descripcion']
        empresa.cargo = validated_data['cargo']
        empresa.save()
        return empresa 

class planSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['nombre','precio','description','documentos','reportes','soporte','firma','usuarios','clientes']
