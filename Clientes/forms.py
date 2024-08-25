from django import forms
from .models import Cliente   # Importa el modelo de Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'documento', 'telefono', 'email', 'direccion', 'nivel']  # Campos del formulario