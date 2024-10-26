from django import forms
from .models import Costos,Tipos,Parametros, Organizacion

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


class ParametroForm(forms.ModelForm):

     class Meta:
        model = Parametros
        fields = ['nombre', 'porcentaje'] 


class OrganizacionForm(forms.ModelForm):
    class Meta:
        model = Organizacion
        fields = ['razonSocial', 'NIT', 'direccion', 'correoElectronico', 'telefono']
