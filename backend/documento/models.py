from django.db import models
import base64



# Create your models here.
class Documentos(models.Model):
    _file = models.BinaryField(db_column='file')
    content_type = models.CharField(max_length=100, null=True)
    nombreDoc = models.CharField(max_length=100, null = False)
    #fechaEmision = models.DateTimeField(null=True)
    hora = models.TimeField(auto_now_add=True)
    tipoDocumento = models.CharField(max_length=50)
    #cliente = models.ForeignKey(User,on_delete=models.SET_DEFAULT("cliente"))
    #proveedor = models.ForeignKey(Empresa,on_delete=models.SET_NULL)
    estado  = models.CharField(max_length=25)
    tipoCreacion = models.CharField(max_length=25)

    def set_data(self, file):
        self._file = base64.encodestring(file)

    def get_data(self):
        return base64.decodestring(self._file)

    file = property(get_data, set_data)