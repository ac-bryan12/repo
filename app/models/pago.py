from django.db import models
from .tipoPago import TipoPago
from .empresa_plan import EmpresaPlan
from .detallePago import DetallePago

class Pago(models.Model):
    monto = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)
    detallePago = models.ForeignKey(DetallePago,on_delete=models.SET_NULL,null=True)
    tipoPago = models.ForeignKey(TipoPago,on_delete=models.SET_NULL,null=True)
    empresa_plan = models.ForeignKey(EmpresaPlan,on_delete=models.SET_NULL,null=True)
