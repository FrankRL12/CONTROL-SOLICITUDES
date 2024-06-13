from django.contrib import admin
from .models import Reporte

# Register your models here.
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_completo','departamento','servicio_solicitado',
                    'servicio_realizado', 'observacion', 'tecnico', 'fecha', 'hora', 'estado', 'prioridad')
    

admin.site.register(Reporte, ReporteAdmin)