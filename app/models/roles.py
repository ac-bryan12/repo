from django.db import models

class Rol(models.Model):
    codigo = models.CharField(max_length=30,blank=False)
    nombre = models.CharField(max_length=30,blank=False)
