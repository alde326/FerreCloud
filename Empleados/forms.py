from django import forms
from .models import Empleado  # Importa el modelo de Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'documento', 'telefono', 'email', 'direccion', 'salario', 'cajaDeCompensacion', 'cargo', 'estado']  # Campos del formulario