from django.db import models
from datetime import datetime

# Create your models here.
# Función personalizada para obtener la hora actual
def obtener_hora_actual():
    return datetime.now().time()


class Historial(models.Model):
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
    
    usuario = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=30)
    departamento = models.CharField(max_length=100)
    servicio_solicitado = models.TextField()
    servicio_realizado = models.CharField(max_length=100)
    observacion = models.TextField()
    tecnico = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(default=datetime.now().time())
    fecha_final = models.DateField(auto_now_add=True)
    hora_final= models.TimeField(default=obtener_hora_actual)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    prioridad = models.CharField(max_length=100, choices=PRIORIDAD_CHOICES)