from django.contrib import admin
from .models import Historial

# Register your models here.
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('usuario','nombre_completo', 'departamento','servicio_solicitado',
                    'servicio_realizado', 'observacion', 'tecnico', 'fecha', 'hora','fecha_final', 'hora_final', 'estado', 'prioridad')


admin.site.register(Historial, HistorialAdmin)