from django.db import models

class Tipos(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Costos(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.ForeignKey(Tipos, on_delete=models.CASCADE, default=1)  # Llave foránea a Tipos
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre



    
