from django.db import models

class Costos(models.Model):
    nombre = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    frecuente = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class CostosFrecuentes(models.Model):
    nombre = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre      
