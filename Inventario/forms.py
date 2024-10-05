from django import forms
from .models import Producto  # Importa el modelo de Empleado

class ProductForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'presentacion', 'stockM', 'cantidad', 'precio', 'proveedor', 'costo', 'observacion']  # Campos del formulario