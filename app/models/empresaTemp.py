from django.db import models
from django.db.models.fields import UUIDField
import uuid

class EmpresaTemp(models.Model):
    razonSocial =  models.TextField(max_length=150,blank=False)
    direccion = models.CharField(max_length=30,blank= False)
    telefono = models.PositiveBigIntegerField(blank=False)
    correo = models.EmailField(max_length=150, blank=False)
    token = models.UUIDField(max_length=36,default=uuid.uuid4)