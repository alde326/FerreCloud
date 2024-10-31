from django.db import models

class Tipos(models.Model):
    nombre = models.CharField(max_length=255)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre



class Costos(models.Model):
    nombre = models.CharField(max_length=255)
    ingreso_egreso = models.BooleanField(default=False)
    tipo = models.ForeignKey(Tipos, on_delete=models.CASCADE, default=1)  # Llave foránea a Tipos
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre



class Organizacion(models.Model):
    razonSocial = models.CharField(max_length=255)
    NIT = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    correoElectronico = models.EmailField(max_length=254, unique=True)
    telefono = models.CharField(max_length=255)



class Parametros(models.Model):
    nombre = models.CharField(max_length=255)
    porcentaje =   models.DecimalField(max_digits=15, decimal_places=5)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre