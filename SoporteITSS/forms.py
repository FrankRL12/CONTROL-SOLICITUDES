from django import forms
from solicitud .models import Solicitar

class SolicitudForm(forms.Form):
    detalle_equipo = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingresar El detalle del Equipo',
        'class': 'form-control'
    }), required=True)  # Indicar que este campo es requerido

    descripcion = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Ingresar la descripción',
        'class': 'form-control'
    }), required=True)  # Indicar que este campo es requerido

    OPCIONES_MANTENIMIENTO = (
        ('Soporte', 'Soporte'),
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Mantenimiento', 'Mantenimiento'),
    )
    mantenimiento = forms.ChoiceField(choices=OPCIONES_MANTENIMIENTO, widget=forms.Select(attrs={
        'class': 'form-control'
    }), required=True)  # Indicar que este campo es requerido


    

