from django.db import models

class TipoPago(models.Model):
    nombre = models.TextField(max_length=50,blank=False)