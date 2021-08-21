from django.db import models

class EstadoPlan(models.Model):
    nombre = models.CharField(max_length=30,blank=False)