from django import forms
from .models import Proveedor
from Inventario.models import Producto
from .models import Reabastecimiento

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nit', 'razonSolcial', 'telefono', 'email', 'direccion', 'nombreContacto', 'celular']  # Campos del formulario


