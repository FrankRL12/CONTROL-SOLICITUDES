from django.db import models
from datetime import datetime
from usuario.models import Usuario

# Create your models here.
def obtener_hora_actual():
    return datetime.now().time()


class Reporte(models.Model):
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
    nombre_completo = models.CharField(max_length=30)
    departamento = models.CharField(max_length=100)
    servicio_solicitado = models.TextField()
    servicio_realizado = models.CharField(max_length=100)
    observacion = models.TextField()
    tecnico = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(default=datetime.now().time())
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    prioridad = models.CharField(max_length=100, choices=PRIORIDAD_CHOICES, default=BAJA)