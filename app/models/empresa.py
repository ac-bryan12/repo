from django.db import models

class Empresa(models.Model):
    ruc = models.IntegerField(primary_key=True)
    razonSocial =  models.TextField(max_length=50,blank=False)
    direccion = models.CharField(max_length=30,blank= False)
    telefono = models.IntegerField(blank=False)