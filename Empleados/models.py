from django.db import models

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.CharField(max_length=255, null=True, blank=True)  
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    cajaDeCompensacion = models.CharField(max_length=100, null=True, blank=True)  
    cargo = models.CharField(max_length=100, default=2 )  
    estado = models.BooleanField(default=True)  
    eliminado = models.BooleanField(default=False)
