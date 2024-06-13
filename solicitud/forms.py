from django import forms
from reporte. models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['servicio_realizado', 'observacion', 'tecnico', 'estado']

    def clean_servicio_realizado(self):
        servicio_realizado = self.cleaned_data['servicio_realizado']
        if not servicio_realizado:
            raise forms.ValidationError("El campo 'Servicio Realizado' es obligatorio.")
        return servicio_realizado

    def clean_observacion(self):
        observacion = self.cleaned_data['observacion']
        if not observacion:
            raise forms.ValidationError("El campo 'Observación' es obligatorio.")
        return observacion

    def clean_tecnico(self):
        tecnico = self.cleaned_data['tecnico']
        if not tecnico:
            raise forms.ValidationError("El campo 'Técnico' es obligatorio.")
        return tecnico