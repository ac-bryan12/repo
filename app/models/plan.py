from django.db import models

class Plan(models.Model):
    nombre = models.CharField(max_length=30,blank=False)
    precio = models.FloatField(blank=False)
    descripcion = models.TextField(max_length=250,blank=False)