from django.db import models

class EmpresaTemp(models.Model):
    razonSocial =  models.TextField(max_length=150,blank=False)
    direccion = models.CharField(max_length=30,blank= False)
    telefono = models.IntegerField(blank=False)
    correo = models.EmailField(max_length=150, blank=False)