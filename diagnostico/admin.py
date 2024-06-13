from django.contrib import admin
from .models import Diagnostico

# Register your models here.
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('id','nombre', 'marca', 'n_serie', 'modelo', 'ubicacion', 'diagnostico', 'solucion', 'estado')


admin.site.register(Diagnostico, DiagnosticoAdmin)