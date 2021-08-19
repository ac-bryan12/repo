from django.db import models

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
    