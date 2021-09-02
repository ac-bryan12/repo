from django.db import models

class Empresa(models.Model):

    correo = models.EmailField(max_length=150, blank=True)
    ruc = models.PositiveBigIntegerField(primary_key=True)
    razonSocial =  models.CharField(max_length=150,blank=True)
    direccion = models.CharField(max_length=30,blank= True)
    telefono = models.PositiveBigIntegerField(blank=True)
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
    

