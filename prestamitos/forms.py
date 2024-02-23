from django.forms import ModelForm
from .models import Cliente, Prestamo, Pago


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']
        
   
class PrestamoForm(ModelForm):
    class Meta:
        model = Prestamo
        fields = ['cliente', 'monto', 'fecha_prestamo', 'tasa_interes', 'plazo_dias']
        
class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['prestamo', 'monto_pago', 'fecha_pago']