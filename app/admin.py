from django.contrib import admin
from django.contrib.admin.decorators import action
from django.template.loader import get_template
from .models.profile import Profile
from .models.empresa import Empresa
from .models.empresa_plan import EmpresaPlan
from .models.detallePago import DetallePago
from .models.estadoPlan import EstadoPlan
from .models.pago import Pago
from .models.plan import Plan
from .models.tipoPago import TipoPago
from app.models.roles import Rol
from app.views.correo import send_mail
from django.views.decorators.csrf import *
from .models.empresaTemp import EmpresaTemp

# Register your models here.


def envioCorreoTemp(modeladmin,request,queryset):
        for empresa in queryset:
                send_mail(empresa.correo,empresa.razonSocial)

@csrf_exempt
@admin.register(EmpresaTemp)
class EmpresaTempAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'modified'
    )
    list_display = (
            'id','razonSocial', 'direccion', 'telefono', 'correo',
            )
    readonly_fields = (
            'id','razonSocial', 'direccion', 'telefono', 'correo', 
            )
    actions= [envioCorreoTemp]

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'modified'
    )
    list_display = (
            'ruc','razonSocial', 'direccion', 'telefono', 'correo',
            )
    readonly_fields = (
            'razonSocial', 'direccion', 'telefono', 'correo', 
            )
    actions= []

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','user','direccion','telefono','cargoEmpres','firmaElectronica','empresa',
        )


@admin.register(EstadoPlan)
class EstadoPlanAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','nombre',
        )

@admin.register(TipoPago)
class TipoPagoAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','nombre',
        )
      
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','codigo','nombre',
        )


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','nombre','precio','description','documentos','reportes','soporte','firma','usuarios','clientes'
        )

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','monto','fecha','detallePago','tipoPago','empresa_plan',
        )

@admin.register(EmpresaPlan)
class EmpresaPlanAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','empresa','user','fechaRegistro','plan','estado',
        )

@admin.register(DetallePago)
class PagoAdmin(admin.ModelAdmin):
        date_heirarchy = {
                'modified'
        }
        list_display = (
                'id','codigoTransaccion',
        )

