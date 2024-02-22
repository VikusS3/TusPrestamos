from django.forms import ModelForm, forms
from .models import Cliente, Prestamo, Pago


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']
        
   