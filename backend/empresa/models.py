from django.contrib.auth.models import User
from django.db import models
import uuid
import base64

class DetallePago(models.Model):
    codigoTransaccion = models.PositiveIntegerField(blank=False)

class Empresa(models.Model):
    correo = models.EmailField(max_length=150, blank=True)
    ruc = models.CharField(max_length=150,primary_key=True)
    razonSocial =  models.CharField(max_length=150,blank=True)
    direccion = models.CharField(max_length=150,blank= True)
    telefono = models.CharField(max_length=13,blank=True)
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

class Plan(models.Model):
    nombre = models.CharField(max_length=30,blank=False)
    precio = models.FloatField(blank=False)
    description = models.TextField(max_length=150, blank=False)
    documentos = models.TextField(max_length=150, blank = False)
    reportes = models.IntegerField(blank=False)
    soporte = models.TextField(max_length=50, blank = False)
    firma = models.TextField(max_length=50,blank=False)
    usuarios = models.TextField(max_length=50,blank=False)
    clientes = models.TextField(max_length=50,blank=False)

class EstadoPlan(models.Model):
    nombre = models.CharField(max_length=30,blank=False)

class EmpresaPlan(models.Model):
    empresa = models.ForeignKey(Empresa,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True,null=False)
    plan = models.ForeignKey(Plan,on_delete=models.SET_NULL,null=True)
    estado = models.ForeignKey(EstadoPlan,on_delete=models.SET_NULL,null=True)


class EmpresaTemp(models.Model):
    razonSocial =  models.TextField(max_length=150,blank= True)
    # direccion = models.CharField(max_length=150,blank= True)
    telefono = models.CharField(max_length=13,blank=True)
    correo = models.EmailField(max_length=150, blank=True)
    token = models.UUIDField(max_length=150,default=uuid.uuid4)
    cargo = models.CharField(max_length=150,blank=True)
    nombre = models.CharField(max_length=150,blank=True)
    descripcion = models.CharField(max_length=250,blank=True)
    
class TipoPago(models.Model):
    nombre = models.TextField(max_length=50,blank=False)

class Pago(models.Model):
    monto = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)
    detallePago = models.ForeignKey(DetallePago,on_delete=models.SET_NULL,null=True)
    tipoPago = models.ForeignKey(TipoPago,on_delete=models.SET_NULL,null=True)
    empresa_plan = models.ForeignKey(EmpresaPlan,on_delete=models.SET_NULL,null=True)


class Documentos(models.Model):
    _file = models.BinaryField(db_column='file')
    content_type = models.CharField(max_length=100, null=True)
    nombreDoc = models.CharField(max_length=100, null = False)
    #fechaEmision = models.DateTimeField(null=True)
    hora = models.TimeField(auto_now_add=True)
    tipoDocumento = models.CharField(max_length=50)
    #cliente = models.ForeignKey(User,on_delete=models.SET_DEFAULT("cliente"))
    #proveedor = models.ForeignKey(Empresa,on_delete=models.SET_NULL)
    estado  = models.CharField(max_length=25)
    tipoCreacion = models.CharField(max_length=25)

    def set_data(self, file):
        self._file = base64.encodestring(file)

    def get_data(self):
        return base64.decodestring(self._file)

    file = property(get_data, set_data)


