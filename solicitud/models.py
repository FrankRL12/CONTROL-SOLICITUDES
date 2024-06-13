from django.db import models
from datetime import datetime
from usuario.models import Usuario

# Create your models here.
# Función personalizada para obtener la hora actual
def obtener_hora_actual():
    return datetime.now().time()


class Solicitar(models.Model):
    EN_ESPERA = 'En espera'
    ACEPTADO = 'Aceptado'
    CANCELADO = 'Cancelado'
    EN_PROCESO = 'En proceso'
    FINALIZADO = 'Finalizado'


    ESTADO_CHOICES = [
        (EN_ESPERA, 'En espera'),
        (ACEPTADO, 'Aceptado'),
        (CANCELADO, 'Cancelado'),
        (EN_PROCESO, 'En proceso'),
        (FINALIZADO, 'Finalizado'),
    ]


    BAJA = 'Baja'
    MEDIA = 'Media'
    ALTA = 'Alta'

    PRIORIDAD_CHOICES = [
        (BAJA, 'Baja'),
        (MEDIA, 'Media'),
        (ALTA, 'Alta'),
    ]

    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    departamento=  models.CharField(max_length=100)
    detalle_equipo= models.CharField(max_length=100)
    descripcion= models.TextField()
    mantenimiento= models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=EN_ESPERA)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(default=obtener_hora_actual)
    prioridad = models.CharField(max_length=100, choices=PRIORIDAD_CHOICES, default=BAJA)