from django import forms
from .models import Proveedor  # Importa el modelo de Empleado
from .models import Reabastecimiento

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nit', 'razonSolcial', 'telefono', 'email', 'direccion', 'nombreContacto', 'celular']  # Campos del formulario

class ReabastecimientoForm(forms.ModelForm):
    class Meta:
        model = Reabastecimiento
        fields = ['proveedor', 'producto', 'cantidad', 'credito', 'observaciones']
        widgets = {
            'credito': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escribe cualquier observación aquí...'
            }),
        }