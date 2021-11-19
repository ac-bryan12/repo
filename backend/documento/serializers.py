from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotAcceptable
from .models import Documentos
from rest_framework import serializers


class DocumentosSerializer(serializers.ModelSerializer):
    _file = serializers.ReadOnlyField()
    content_type = serializers.CharField(max_length=150)
    nombreDoc = serializers.CharField(max_length=150)
    #fechaEmision = serializers.DateTimeField(allow_null = True, required = False)
    hora = serializers.TimeField(required = False)
    tipoDocumento = serializers.CharField(max_length=150,required = False)
    #cliente = serializers.CharField()
    #proveedor = models.ForeignKey(Empresa,on_delete=models.SET_NULL)
    estado  = serializers.CharField(max_length=25,required = False)
    tipoCreacion = serializers.CharField(max_length=25,required = False)
    class Meta:
        model = Documentos
        fields = ['id','_file','content_type','nombreDoc','hora','tipoDocumento','estado','tipoCreacion']


    def validate(self, attrs):
        return super().validate(attrs)


class InfoTributariaSerializer(serializers.Serializer):
    ambiente = serializers.RegexField("^[0-9]+$",max_length=1)		
    tipoEmision	= serializers.RegexField("^[0-9]+$",max_length=2)	
    razonSocial	 =  serializers.CharField(max_length=300)		
    nombreComercial	= serializers.CharField(max_length=300,required=False)		
    ruc = serializers.RegexField("^[0-9]+$",max_length=13)		 		
    claveAcceso	= serializers.RegexField("^[0-9]+$",max_length=49)			
    codDoc = serializers.RegexField("^[0-9]+$",max_length=2)		 	 		
    estab = serializers.RegexField("^[0-9]+$",max_length=3)	 	 	 		
    ptoEmi = serializers.RegexField("^[0-9]+$",max_length=3)		 		
    secuencial = serializers.RegexField("^[0-9]+$",max_length=9)		 		
    dirMatriz = serializers.RegexField("^[0-9]+$",max_length=300)

    ############valida oets valida!!!


class InfoFacturaGeneral(serializers.Serializer):
    fechaEmision = serializers.DateTimeField(input_formats='%d/%m/%Y')
    dirEstablecimiento = serializers.CharField(required = False, max_length = 300)
    contribuyenteEspecial = serializers.CharField(required = False, max_length = 13)
    obligadoContabilidad = serializers.ChoiceField(required = False, choices=["NO","YES"])
    tipoIdentifiacionComprador = serializers.CharField(max_length=2)
    identificacionComprador = serializers.CharField(max_length = 20)
    totalSinImpuestos = serializers.DecimalField(decimal_places=2,max_digits=14)
    totalDescuento = serializers.DecimalField(decimal_places=2,max_digits=14)
    guiaRemision = serializers.RegexField("^[0-9]+$",required = False, max_length=15)
    direccionComprador = serializers.CharField(required=False, max_length = 300)

    ################validaa oets valida!!!!
    def validate_tipoIdentificacionComprador(self, value):
        if not value=="04" or not value=="05" or not value=="06" or not value=="07" or not value=="08":
            raise NotAcceptable({'error':'El campo del tipo de identificacion no es correcto, por favor verifíquelo'}) 
        return value
       
            


class FacturaSerializer(serializers.Serializer):
    infoTributaria = InfoTributariaSerializer()
    