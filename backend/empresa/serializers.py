from empresa.models import Empresa,EmpresaTemp,Plan
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _



class EmpresaSerializer(serializers.ModelSerializer):
    ruc = serializers.CharField(max_length=13)
    razonSocial =  serializers.CharField(min_length=5,max_length=50)
    direccion = serializers.CharField(max_length=30)
    telefono = serializers.CharField(max_length=10,min_length=10)
    correo =  serializers.EmailField(min_length=7,required=False)

    class Meta:
        model = Empresa
        fields = ['ruc', 'razonSocial','direccion','telefono','correo']

    def validate(self, attrs):
        print(attrs)
        msg:any
        if not self.instance:
            if Empresa.objects.filter(ruc=attrs['ruc']).exists() :
                msg = _("El Ruc ingresado ya existe en el sistema")
            elif Empresa.objects.filter(correo=attrs['correo']).exists() :
                msg = _("El email ingresado ya existe en el sistema")
            else :
                return attrs
        else:
            return attrs
        raise serializers.ValidationError(msg)
        

    def create(self,validated_data):
        print(validated_data)
        empresa:Empresa = Empresa()
        print("crear empresa")
        empresa.ruc = validated_data['ruc']
        empresa.razonSocial = validated_data['razonSocial']
        empresa.correo = validated_data['correo']
        empresa.direccion = validated_data['direccion']
        empresa.telefono = validated_data['telefono']
        empresa.save()
        return empresa 

    def update(self, instance, validated_data):
        print(validated_data)
        print("actualizar empresa")
        instance.correo = validated_data['correo']
        instance.direccion = validated_data['direccion']
        instance.telefono = validated_data['telefono']
        instance.save()
        return instance

class EmpresaTempSerializer(serializers.ModelSerializer):
    razonSocial =  serializers.CharField(min_length=5,max_length=50)
    # direccion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=10,min_length=10)
    correo =  serializers.EmailField(min_length=7,required=False)

    class Meta:
        model = Empresa
        fields = ['razonSocial','telefono','correo']

    def validate(self, attrs):
        msg:any
        if EmpresaTemp.objects.filter(correo=attrs['correo']).exists() :
            msg = _("el email ingresado ya existe en el sistema")
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

class planSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['nombre','precio','description','documentos','reportes','soporte','firma','usuarios','clientes']
