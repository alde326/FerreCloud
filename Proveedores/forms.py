from django import forms
from .models import Proveedor
from Inventario.models import Producto
from .models import Reabastecimiento, ReabastecimientoDetalle

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nit', 'razonSolcial', 'telefono', 'email', 'direccion', 'nombreContacto', 'celular']  # Campos del formulario


class ReabastecimientoForm(forms.ModelForm):
    class Meta:
        model = Reabastecimiento
        fields = ['proveedor', 'fechaEsperada', 'credito', 'observaciones']

class ReabastecimientoDetalleForm(forms.ModelForm):
    class Meta:
        model = ReabastecimientoDetalle
        fields = ['producto', 'cantidad', 'observaciones']
    
    def __init__(self, *args, **kwargs):
        proveedor = kwargs.pop('proveedor', None)
        super().__init__(*args, **kwargs)
        if proveedor:
            self.fields['producto'].queryset = Producto.objects.filter(proveedor=proveedor)

ReabastecimientoDetalleFormSet = forms.inlineformset_factory(
    Reabastecimiento, 
    ReabastecimientoDetalle, 
    form=ReabastecimientoDetalleForm, 
    extra=1,  # Muestra un formulario adicional vacío
    can_delete=True
)


