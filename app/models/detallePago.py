from django.db import models

class DetallePago(models.Model):
    codigoTransaccion = models.PositiveIntegerField(blank=False)