from django import forms
from .models import Costos,Tipos  # Importa el modelo de Empleado

class CostosForm(forms.ModelForm):

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Costos
        fields = ['nombre', 'valor', 'tipo', 'fecha', 'descripcion', 'eliminado']  # Campos del formulario


class TipoForm(forms.ModelForm):

    class Meta:
        model = Tipos
        fields = ['nombre']  # Campos del formulario