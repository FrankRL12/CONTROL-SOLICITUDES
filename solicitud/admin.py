from django.contrib import admin
from .models import Solicitar

# Register your models here.

class SolicitarAdmin(admin.ModelAdmin):
    list_display = ('usuario','nombre', 'apellido', 'departamento', 'detalle_equipo', 'descripcion',
                    'mantenimiento', 'estado', 'fecha', 'hora', 'prioridad')


admin.site.register(Solicitar, SolicitarAdmin)