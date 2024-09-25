from django import forms
from .models import Costos  # Importa el modelo de Empleado

class CostosForm(forms.ModelForm):

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Costos
        fields = ['nombre', 'valor', 'fecha', 'descripcion', 'frecuente', 'eliminado']  # Campos del formulario