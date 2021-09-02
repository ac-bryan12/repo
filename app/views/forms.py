from django import forms
from app.models.empresa import Empresa

class EmpresaForms(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['ruc','razonSocial','direccion','telefono','correo']

        