from django.db import models
from Inventario.models import Producto
from Clientes.models import Cliente

class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total_con_iva = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.TextField(null=True, blank=True)
    pagoElectronico = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Factura {self.id} - {self.fecha.strftime('%d/%m/%Y %H:%M:%S')}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    devuelto = models.BooleanField(default=False) 
    cantidad_devuelta = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Detalle {self.id} - {self.producto.nombre}"