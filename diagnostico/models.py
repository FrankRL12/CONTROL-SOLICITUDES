from django.db import models

# Create your models here.
class Diagnostico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    marca = models.CharField(max_length=50)
    n_serie = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=30)
    diagnostico = models.TextField()
    solucion = models.TextField()
    estado = models.CharField(max_length=20, choices=(('activo', 'activo'), ('en reparacion', 'en reparacion'), ('de vaja', 'de vaja')))