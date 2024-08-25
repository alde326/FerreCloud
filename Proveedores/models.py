from django.db import models
from Inventario.models import Producto

class Proveedor(models.Model):
    nit = models.CharField(max_length=100)
    razonSolcial = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.CharField(max_length=255, null=True, blank=True) 
    nombreContacto = models.CharField(max_length=100)
    celular = models.CharField(max_length=20)
    eliminado = models.BooleanField(default=False)


class Reabastecimiento(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    credito = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=200)
    #llegada
    #fecha de llegada
    #

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades'