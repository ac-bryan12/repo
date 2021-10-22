from django.contrib.auth.models import User
from django.db import models
import uuid

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
    razonSocial =  models.TextField(max_length=150,blank=False)
    direccion = models.CharField(max_length=30,blank= False)
    telefono = models.PositiveBigIntegerField(blank=False)
    correo = models.EmailField(max_length=150, blank=False)
    token = models.UUIDField(max_length=36,default=uuid.uuid4)
    
class TipoPago(models.Model):
    nombre = models.TextField(max_length=50,blank=False)

class Pago(models.Model):
    monto = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)
    detallePago = models.ForeignKey(DetallePago,on_delete=models.SET_NULL,null=True)
    tipoPago = models.ForeignKey(TipoPago,on_delete=models.SET_NULL,null=True)
    empresa_plan = models.ForeignKey(EmpresaPlan,on_delete=models.SET_NULL,null=True)
