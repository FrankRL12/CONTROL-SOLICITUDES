from django import forms
from .models import Diagnostico

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['nombre', 'marca', 'n_serie', 'modelo', 'ubicacion', 'diagnostico', 'solucion', 'estado']
        widgets = {
            'estado': forms.Select(choices=[('activo', 'Activo'), ('en reparación', 'En reparación'), ('de baja', 'De baja')])
        }
