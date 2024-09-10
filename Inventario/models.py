from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    presentacion = models.CharField(max_length=20)
    stockM = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proveedor = models.ForeignKey('Proveedores.Proveedor', on_delete=models.CASCADE)
    observacion = models.CharField(max_length=100, null=True, blank=True)
    eliminado = models.BooleanField(default=False)