from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True)
    documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    direccion = models.CharField(max_length=255, null=True, blank=True)
    nivel = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    eliminado = models.BooleanField(default=False)