from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
import base64

class TipoDocumento(models.Model):
    name = models.CharField(max_length=100)
    
class Estado(models.Model):
    name = models.CharField(max_length=150)
    
class TipoCreacion(models.Model):
    name = models.CharField(max_length=150)

class Documentos(models.Model):
    id = models.AutoField(primary_key=True,validators=[MaxValueValidator(999999999)])
    _file = models.BinaryField(db_column='file',null=True)
    pdf = models.BinaryField(null=True)
    content_type = models.CharField(max_length=100, null=True)
    nombreDoc = models.CharField(max_length=100, null = True)
    fechaEmision = models.DateTimeField(auto_now=True)
    # hora = models.TimeField(auto_now_add=True)
    tipoDocumento = models.ForeignKey(TipoDocumento,on_delete=models.PROTECT,null=True)
    cliente = models.ForeignKey(User,related_name="documento_cliente",on_delete=models.PROTECT,null=True)
    proveedor = models.ForeignKey(User,related_name="documento_proveedor",on_delete=models.PROTECT,null=True)
    estado  = models.ForeignKey(Estado,on_delete=models.PROTECT,null=True)
    tipoCreacion = models.ForeignKey(TipoCreacion,on_delete=models.PROTECT,null=True)

    def set_data(self, file):
        self._file = base64.encodestring(file)

    def get_data(self):
        return base64.decodestring(self._file)

    file = property(get_data, set_data)
    
