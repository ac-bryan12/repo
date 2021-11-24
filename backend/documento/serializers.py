from rest_framework.exceptions import NotAcceptable
from .models import Documentos
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

LISTA_PORCENTAJE_ICE=[3041,3041,3041,3073,3075,3077,3078,3079,3080,3081,3092,3610,3620,3630,3640,3660,3093,3101,3053,3054,3111,3043,3033,3671,3684,3686,3688,3691,3692,3695,3696,3698,3682,3681,3680,3533,3541,3541,3541,3542,3543,3544,3581,3582,3710,3720,3730,3740,3871,3873,3874,3875,3876,3877,3878,3601,3552,3553,3602,3545,3532,3671,3771,3685,3687,3689,3690,3693,3694,3697,3699,3683]
LISTA_PORCENTAJE_IVA=[0,2,3,6,7]


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


#Por validar! - B
class InfoTributariaSerializer(serializers.Serializer):
    #ambiente = serializers.IntegerField()		
    #tipoEmision	= serializers.IntegerField()	
    #razonSocial	 =  serializers.CharField(max_length=300)		
    #nombreComercial	= serializers.CharField(max_lentgh=300,required=False)		
    #ruc = serializers.IntegerField(max_value = 9999999999999)		 		
    #claveAcceso	= serializers.CharField(max_length=49)			
    codDoc = serializers.ChoiceField(choices=["01","03","04","05","06","07"])		 	 		
    estab = serializers.IntegerField(max_value = 999)	 	 	 		
    ptoEmi = serializers.IntegerField(max_value = 999)		 		
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
            if codigo == "01": 
                return attrs
        raise NotAcceptable({'error':'El campo del Tipo de Emisión no es correcto, por favor verifíquelo'}) 



#Datos para la etiqueta de InfoFactura - B
class TotalImpuesto(serializers.Serializer):
    codigo = serializers.ChoiceField(required=True,choices=[2,3,5]).error_messages({"invalid_choice": _('"{input}" no es un codigo correcto')})
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
    totalImpuesto = TotalImpuesto()

class Pago(serializers.Serializer): #B
    formaPago = serializers.ChoiceField(required=True,choices=[1,15,16,17,18,19,20,21]).error_messages({"invalid_choice": _('"{input}" no es una forma de pago correcta')})
    total = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    plazo = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)
    unidadTiempo = serializers.CharField(required =False, max_length = 10)

class Pagos(serializers.Seriliazer):#B
    pago = Pago()
    

##Informacion de la etiqueta de InfoFactura 
class InfoFacturaGeneral(serializers.Serializer): #B
    #fechaEmision = serializers.DateTimeField(required =True, input_formats='%d/%m/%Y')
    dirEstablecimiento = serializers.CharField(required = False, max_length = 300)
    contribuyenteEspecial = serializers.CharField(required = False, max_length = 13)
    obligadoContabilidad = serializers.ChoiceField(required = False, choices=["NO","YES"])
    tipoIdentifiacionComprador = serializers.CharField(required =True, max_length=2)
    identificacionComprador = serializers.CharField(required =True, max_length = 20)
    totalSinImpuestos = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    totalDescuento = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    guiaRemision = serializers.IntegerField(required = False, max_value=999999999999999) #tener en cuenta
    #direccionComprador = serializers.CharField(requeired=False, max_length = 300)
    totalConImpuesto = TotalConImpuestos(many = True)
    propina = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    importeTotal = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    moneda = serializers.CharField(required = True, max_length = 15)
    pagos = Pagos(many=True)
    valorRetIva = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)
    valorRetRenta = serializers.DecimalField(required =False, decimal_places=2,max_digits=14)


    def validate_identificacionComprador(self,attrs):
        tipo  = attrs['tipoIdentificacionComprador'] 
        if tipo == "04":
            #validacion del ruc
            return attrs
        if tipo =="05":
            #validacion cedula
            return attrs
        if tipo == "07":
            if tipo.length == 13 and attrs["identificacionComprador"] == "9999999999999":
                return attrs
            else:
                raise NotAcceptable({'error':'El campo de identificacion no concuerda con el tipo de identificacion de consumidor final'}) 
        raise NotAcceptable({'error':'El campo del tipo de identificacion no es correcto, por favor verifíquelo'})  

#Datos para la etiqueta Detalles #B
class Impuesto(serializers.Serializer):
    codigo = serializers.ChoiceField(required=True,choices=[2,3,5]).error_messages({"invalid_choice": _('"{input}" no es un codigo correcto')})
    codigoPorcentaje = serializers.IntegerField(required=True,max_value=9999)
    tarifa = serializers.IntegerField(required =True,min_length = 1,max_length = 4 )
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
    impuesto = Impuesto()

class DetalleAdicional(serializers.Serializer): #B
    nombre = serializers.CharField(required = True)
    valor = serializers.CharField(required = True)

class DetallesAdicionales(serializers.Serializer): #B
    detAdicional = DetalleAdicional()

class Detalle(serializers.Serializer): #B
    codigoPrincipal = serializers.CharField(required = True,max_length = 25)
    codigoAuxiliar = serializers.CharField(required = False, max_length = 25)
    descripcion = serializers.CharField(requiered = True, max_length = 300)
    cantidad = serializers.DecimalField(required =True, decimal_places=6,max_digits=18)
    precioUnitario = serializers.DecimalField(required =True, decimal_places=6,max_digits=18)
    descuento = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    precioTotalSinImpuesto = serializers.DecimalField(required =True, decimal_places=2,max_digits=14)
    detallesAdicionales = DetallesAdicionales(required =False, many = True)
    impuestos = Impuestos(many=True)

##Informacion de la etiqueta de Detalles
class Detalles(serializers.Serializer): #B
    detalle = Detalle()



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
    nombre = serializers.CharField(max_length=300)

##Informacion de la etiqueta InfoAdicional 
class InfoAdicional(serializers.Serializer):
    campoAdicional = CampoAdicional(required=False)


class FacturaSerializer(serializers.Serializer):
    infoTributaria = InfoTributariaSerializer()
    infoFactura = InfoFacturaGeneral()
    detalles = Detalles(many=True)
    retenciones = Retenciones(required=False)
    infoAdicional= InfoAdicional(required=False)

    
    