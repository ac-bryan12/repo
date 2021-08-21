from django.contrib import admin
from .models.profile import Profile
from .models.empresa import Empresa
from .models.empresa_plan import EmpresaPlan
from .models.detallePago import DetallePago
from .models.estadoPlan import EstadoPlan
from .models.pago import Pago
from .models.plan import Plan
from .models.tipoPago import TipoPago
from app.models.roles import Rol

# Register your models here.
admin.site.register(Profile)
admin.site.register(Empresa)
admin.site.register(EmpresaPlan)
admin.site.register(DetallePago)
admin.site.register(EstadoPlan)
admin.site.register(Pago)
admin.site.register(Plan)
admin.site.register(TipoPago)
admin.site.register(Rol)

