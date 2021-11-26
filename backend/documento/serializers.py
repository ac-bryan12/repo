from datetime import datetime
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotAcceptable
from rest_framework.fields import FloatField
from .models import Documentos, Estado, TipoCreacion, TipoDocumento
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from usuario.models import Profile

LISTA_PORCENTAJE_ICE=[3041,3041,3041,3073,3075,3077,3078,3079,3080,3081,3092,3610,3620,3630,3640,3660,3093,3101,3053,3054,3111,3043,3033,3671,3684,3686,3688,3691,3692,3695,3696,3698,3682,3681,3680,3533,3541,3541,3541,3542,3543,3544,3581,3582,3710,3720,3730,3740,3871,3873,3874,3875,3876,3877,3878,3601,3552,3553,3602,3545,3532,3671,3771,3685,3687,3689,3690,3693,3694,3697,3699,3683]
LISTA_PORCENTAJE_IVA=[0,2,3,6,7]


class TipoDocSerializador(serializers.Serializer):
    name = serializers.CharField()
    class Meta:
        model = TipoDocumento
        fields = ['name']
class EstadoDocSerializador(serializers.Serializer):
    name = serializers.CharField()
    class Meta:
        model = Estado
        fields = ['name']
    
class TipoCreacionDocSerializador(serializers.Serializer):
    name = serializers.CharField()
    class Meta:
        model = TipoCreacion
        fields = ['name']
    
class DocumentosSerializer(serializers.ModelSerializer):
    _file = serializers.ReadOnlyField()
    content_type = serializers.CharField(max_length=150)
    nombreDoc = serializers.CharField(max_length=150)
    fechaEmision = serializers.DateTimeField(allow_null = True, required = False,read_only=True)
    #hora = serializers.TimeField(required = False)
    cliente = serializers.CharField(read_only=True)
    proveedor = serializers.CharField(read_only=True)
    tipoDocumento = TipoDocSerializador()
    estado  = EstadoDocSerializador()
    tipoCreacion = TipoCreacionDocSerializador()
    class Meta:
        model = Documentos
        fields = ['id','_file','content_type','nombreDoc','fechaEmision','tipoDocumento','estado','tipoCreacion','cliente','proveedor']

    def to_representation(self, instance):
        fechaEmision:datetime = instance.fechaEmision
        representation = super().to_representation(instance)
        representation['fechaEmision'] = str(fechaEmision.date().strftime('%d/%m/%Y'))
        return representation

    def validate(self, attrs):
        return super().validate(attrs)


#Por validar! - B
class InfoTributariaSerializer(serializers.Serializer):
    #ambiente = serializers.IntegerField()		
    #tipoEmision	= serializers.IntegerField()	
    #razonSocial	 =  serializers.CharField(max_length=300)		
    nombreComercial	= serializers.CharField(max_length=300,required=False)		
    #ruc = serializers.IntegerField(max_value = 9999999999999)		 		
    #claveAcceso	= serializers.CharField(max_length=49)			
    codDoc = serializers.ChoiceField(choices=["01","03","04","05","06","07"])		 	 		
    estab = serializers.RegexField("^[0-9]+$",max_length = 3)	 	 	 		
    ptoEmi = serializers.RegexField("^[0-9]+$",max_length = 3)		 		

    #secuencial = serializers.IntegerField(max_value=9)		 		
    #dirMatriz = serializers.CharField(max_length=300)

    #def validated_ambiente(self,attrs):
    #    if attrs["ambiente"] == 1:
    #        return attrs
    #    else:
    #        raise NotAcceptable({'error':'El campo del ambiente no es correcto, por favor verifíquelo'})
    #def validated_data(self,attrs):
    #    if attrs["tipoEmision"] == 1:
    #        return attrs
    #    else:
    #        raise NotAcceptable({'error':'El campo del Tipo de Emisión no es correcto, por favor verifíquelo'})
    def validated_codDoc(self,attrs):
        if attrs["codDoc"]=="":
            codigo = attrs["codDoc"]
            if codigo == 1: 
                return attrs
            elif codigo == 4:
                return attrs
        raise NotAcceptable({'error':'El campo del Tipo de Emisión no es correcto, por favor verifíquelo'}) 

    def create(self, validated_data):
        user =  self.context['owner']
        validated_data['ambiente'] = 1	
        validated_data['tipoEmision']	= 1
        validated_data['razonSocial'] = user.profile.empresa.razonSocial
        validated_data['ruc'] = user.profile.empresa.pk
        return validated_data


#Datos para la etiqueta de InfoFactura - B
class TotalImpuesto(serializers.Serializer):
    codigo = serializers.ChoiceField(required=True,choices=[2,3,5])
    codigoPorcentaje = serializers.IntegerField(required=True,max_value=9999)
    totalDescuento = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)
    baseImponible = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    valor = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    
    def validated_data(self,attrs):
        if attrs["codigo"]==2:
            if attrs["codigoPorcentaje"] in LISTA_PORCENTAJE_IVA:
                return attrs 
            else:
                raise NotAcceptable({'error':'El campo del codigo Porcentaje no pertenece a un codigo admitido, por favor verifíquelo'}) 
        elif attrs["codigo"]==3:
            if attrs["codigoPorcentaje"] in LISTA_PORCENTAJE_ICE:
                return attrs 
            else:
                raise NotAcceptable({'error':'El campo del codigo Porcentaje no pertenece a un codigo admitido, por favor verifíquelo'}) 
        return attrs


class TotalConImpuestos(serializers.Serializer):#B
    totalImpuesto = TotalImpuesto(many=True)

class Pago(serializers.Serializer): #B
    formaPago = serializers.ChoiceField(required=True,choices=["01","15","16","17","18","19","20","21"])
    total = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    plazo = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)
    unidadTiempo = serializers.CharField(required =False, max_length = 10)

class Pagos(serializers.Serializer): #B
    pago = Pago(many=True)
    
##Informacion de la etiqueta de InfoNotaCredito 
class InfoNotaCreditoGeneral(serializers.Serializer):
    #fechaEmision = serializers.DateTimeField(required =True, input_formats='%d/%m/%Y')
    dirEstablecimiento = serializers.CharField(required = False, max_length = 300)
    tipoIdentifiacionComprador = serializers.CharField(required =True) #Integer
    razonSocialComprador = serializers.CharField(max_length= 300)
    identificacionComprador = serializers.CharField(required =True, max_length = 13) #pasaporte ??
    contribuyenteEspecial = serializers.CharField(required = False, max_length = 13)
    obligadoContabilidad = serializers.ChoiceField(required = False, choices=["NO","YES"])
    rise = serializers.CharField(max_length= 40)
    codDocModificado = serializers.ChoiceField(choices=[1,3,4,5,6,7])
    numDocModificado = serializers.CharField(required=False, max_length=15)
    fechaEmisionDocSustento = serializers.DateTimeField(required = True, input_formats='%d/%m/%Y')
    totalSinImpuestos = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    valorModificacion = serializers.DecimalField(required=True, decimal_places=2, max_digits=14)
    moneda = serializers.CharField(required = True, max_length = 15)
    totalConImpuesto = TotalConImpuestos(many = True)
    motivo = serializers.CharField(max_length=300)

    def validate_identificacionComprador(self,attrs):
        tipo  = attrs['tipoIdentificacionComprador'] 
        if tipo == "04":
            #validacion del ruc
            return attrs
        if tipo == "05":
            #validacion cedula
            return attrs
        if tipo == "07":
            if tipo.length == 13 and attrs["identificacionComprador"] == "9999999999999":
                return attrs
            else:
                raise NotAcceptable({'error':'El campo de identificacion no concuerda con el tipo de identificacion de consumidor final'}) 
        raise NotAcceptable({'error':'El campo del tipo de identificacion no es correcto, por favor verifíquelo'})
    

##Informacion de la etiqueta de InfoFactura 
class InfoFacturaGeneral(serializers.Serializer): #B
    #fechaEmision = serializers.DateTimeField(required =True, input_formats='%d/%m/%Y')
    dirEstablecimiento = serializers.CharField(required = False, max_length = 300)
    contribuyenteEspecial = serializers.CharField(required = False, max_length = 13)
    obligadoContabilidad = serializers.ChoiceField(required = False, choices=["NO","SI","no","si","No","Si"])
    tipoIdentificacionComprador = serializers.CharField(required =True, max_length=2)
    identificacionComprador = serializers.CharField(required =True, max_length = 20)
    totalSinImpuestos = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    totalDescuento = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    guiaRemision = serializers.IntegerField(required = False, max_value=999999999999999) #tener en cuenta
    #direccionComprador = serializers.CharField(requeired=False, max_length = 300)
    totalConImpuestos = TotalConImpuestos()
    propina = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    importeTotal = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    moneda = serializers.CharField(required = True, max_length = 15)
    pagos = Pagos()
    valorRetIva = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)
    valorRetRenta = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)


    def validate(self,attrs):
        tipo  = attrs['tipoIdentificacionComprador'] 
        id = attrs['identificacionComprador']
        if tipo == "04":

            #validacion del ruc
            return attrs
        if tipo == "05":
            empresa = self.context['owner'].profile.empresa
            if not Profile.objects.filter(pk=id,empresa=empresa).exists():
                raise ValidationError({"error":"El comprador indicado no consta como su cliente."})
            return attrs
        if tipo == "07":
            if id.length == 13 and id == "9999999999999":

                return attrs
            else:
                raise NotAcceptable({'error':'El campo de identificacion no concuerda con el tipo de identificacion de consumidor final'}) 
        raise NotAcceptable({'error':'El campo del tipo de identificacion no es correcto, por favor verifíquelo'})  

#Datos para la etiqueta Detalles #B
class Impuesto(serializers.Serializer):
    codigo = serializers.ChoiceField(required=True,choices=[2,3,5])
    codigoPorcentaje = serializers.IntegerField(required=True,max_value=9999)
    tarifa = serializers.IntegerField(required =True,max_value = 9999)
    baseImponible = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)
    valor = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)

    def validated_data(self,attrs):
        if attrs["codigo"]==2:
            if attrs["codigoPorcentaje"] in LISTA_PORCENTAJE_IVA:
                return attrs 
            else:
                raise NotAcceptable({'error':'El campo del codigo Porcentaje no pertenece a un codigo admitido, por favor verifíquelo'}) 
        elif attrs["codigo"]==3:
            if attrs["codigoPorcentaje"] in LISTA_PORCENTAJE_ICE:
                return attrs 
            else:
                raise NotAcceptable({'error':'El campo del codigo Porcentaje no pertenece a un codigo admitido, por favor verifíquelo'}) 
        return attrs

class Impuestos(serializers.Serializer): #B
    impuesto = Impuesto(many=True)

class DetalleAdicional(serializers.Serializer): #B
    nombre = serializers.CharField(required = True, max_length=250)
    valor = serializers.CharField(required = True, max_length=50)

class DetallesAdicionales(serializers.Serializer): #B
    detAdicional = DetalleAdicional(required =False)

class Detalle(serializers.Serializer): #B
    codigoPrincipal = serializers.CharField(required = True,max_length = 25)
    codigoAuxiliar = serializers.CharField(required = False, max_length = 25)
    codigoInterno = serializers.CharField(required=False, max_length=25)
    codigoAdicional = serializers.CharField(required=False, max_length=25)
    descripcion = serializers.CharField(required = True, max_length = 300)
    cantidad = serializers.DecimalField(required =True, decimal_places=6,max_digits=18)
    precioUnitario = serializers.DecimalField(required =True, decimal_places=6,max_digits=18)
    descuento = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    precioTotalSinImpuesto = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    detallesAdicionales = DetallesAdicionales(required =False, many = True)
    impuestos = Impuestos()


##Informacion de la etiqueta de Detalles
class Detalles(serializers.Serializer): #B
    detalle = Detalle(many=True)



#Datos para la etiqueta Retenciones
class Retencion(serializers.Serializer):
    codigo = serializers.ChoiceField(required=False,choices=[4])
    codigoPorcentaje = serializers.ChoiceField(required=False,choices = [3,4,5,6,327,328])
    tarifa = serializers.DecimalField(required=False,decimal_places=2, max_digits=5)
    valor = serializers.DecimalField(required=False,decimal_places=2, max_digits=14)


##Informacion de la etiqueta Retenciones
class Retenciones(serializers.Serializer):
    retencion =  Retencion(required=False, many = True)


#Datos para la etiqueta InfoAdicional
class CampoAdicional(serializers.Serializer):
    nombre = serializers.CharField(max_length=250)
    valor = serializers.CharField(max_length=50)

##Informacion de la etiqueta InfoAdicional 
class InfoAdicional(serializers.Serializer):
    campoAdicional = CampoAdicional(required=False,many=True)

#Serializador Factura
class FacturaSerializer(serializers.Serializer):
    infoTributaria = InfoTributariaSerializer()
    infoFactura = InfoFacturaGeneral()
    detalles = Detalles()
    retenciones = Retenciones(required=False)
    infoAdicional= InfoAdicional(required=False)
    
    def create(self, validated_data):
        for factura in validated_data:
            factura['infoTributaria'] = InfoTributariaSerializer.create(self,factura['infoTributaria'])
        return validated_data
    
##Informacion para la Guia de remision
class InfoGuiaRemisionSerializer(serializers.Serializer):
    dirEstablecimiento = serializers.CharField(required= False,max_length=300)
    dirPartida = serializers.CharField(required= True,max_length=300)
    #razonSocialTransportista?
    tipoIdentificacionTransportista = serializers.CharField(required =True, max_length=2)
    rucTransportista = serializers.IntegerField(required =True, max_value = 9999999999999)
    rise = serializers.CharField(required = False, max_length=40)
    obligadoContabilidad = serializers.ChoiceField(required= False, choices=["SI","NO"])
    contribuyenteEspecial = serializers.CharField(required = False, max_length = 13)
    #fecha Inicio  Obligatorio
    #fechaFin Obligatorio
    placa = serializers.CharField(required = False, max_length=20)


##Informacion para la Guia de remision
class DetalleDestinatario(serializers.Serializer):
    codigoInterno = serializers.CharField(required=False,max_length = 25)
    codigoAdicional = serializers.CharField(required=False,max_length = 25)
    descripcion = serializers.CharField(required=True,max_length = 300)
    cantidad = serializers.DecimalField(required=True,decimal_places=6,max_digits=18)
    detallesAdicionales = DetallesAdicionales(required = False,many=True)

class Destinatario(serializers.Serializer):
    identificacionDestinatario = serializers.CharField(required=True,max_length = 13)## pasaporte ? 
    razonSocialDestinatario = serializers.CharField(required=True,max_length = 300)
    dirDestinatario = serializers.CharField(required=True,max_length = 300)
    motivoTraslado = serializers.CharField(required=True,max_length = 300)
    docAduaneroUnico = serializers.CharField(required=False,max_length = 20)
    codEstabDestino = serializers.IntegerField(required=False,max_value = 999)
    ruta = serializers.CharField(required=True,max_length = 300)
    codDocSustento = serializers.ChoiceField(required=False,choices=[1,3,4,5,6,7])
    numDocSustento = serializers.CharField(required=False,max_length = 15)
    numAutDocSustento = serializers.CharField(required=False,min_length = 10,max_length = 49)
    #fechaEmisionDocSustento opcional 
    detalles = DetalleDestinatario(required =True)

##Informacion para la guia de Remision
class Destinarios(serializers.Serializer):
    destinario= Destinatario(required =True)

##Datos la etiqueta de Guia de Remision
class GuiaRemisionSerializer(serializers.Serializer):
    infoTributaria = InfoTributariaSerializer()
    infoGuiaRemision = InfoGuiaRemisionSerializer()
    destinatarios = Destinarios(many=True)
    infoAdicional = InfoAdicional(required =False,many=True)
    def create(self, validated_data):
        for guia in validated_data:
            guia['infoTributaria'] = InfoTributariaSerializer.create(self,guia['infoTributaria'])
        return validated_data


#Serializador Nota Credito
class NotaCreditoSerializer(serializers.Serializer):
    infoTributaria = InfoTributariaSerializer()
    infoNotaCredito = InfoNotaCreditoGeneral()
    detalles = Detalles()
    infoAdicional = InfoAdicional()

    def create(self, validated_data):
        for nota in validated_data:
            nota['infoTributaria'] = InfoTributariaSerializer.create(self,nota['infoTributaria'])
        return validated_data
  
        
class ComprobanteSerializer(serializers.Serializer):
    factura = FacturaSerializer(many=True,required=False)
    notaCredito = NotaCreditoSerializer(many = True, required =False)
    guiaRemision = GuiaRemisionSerializer(many =True, required =False)
    
    def create(self, validated_data):
        #self.context['owner'] = validated_data['owner']
        

        if validated_data.get("factura"):
            validated_data['factura'] = FacturaSerializer.create(self,validated_data['factura'])

        if validated_data.get("guiaRemision"):
            validated_data['guiaRemision'] = FacturaSerializer.create(self,validated_data['guiaRemision'])

        if validated_data.get("notaCredito"):
            validated_data['notaCredito'] = FacturaSerializer.create(self,validated_data['notaCredito'])
        
        return validated_data

