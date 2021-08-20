from django.db import models
from django.contrib.auth.models import User
from .empresa import Empresa
from .estadoPlan import EstadoPlan
from .plan import Plan

class EmpresaPlan(models.Model):
    empresa = models.ForeignKey(Empresa,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    fechaRegistro = models.DateTimeField(auto_now_add=True,null=False)
    plan = models.ForeignKey(Plan,on_delete=models.SET_NULL,null=True)
    estado = models.ForeignKey(EstadoPlan,on_delete=models.SET_NULL,null=True)