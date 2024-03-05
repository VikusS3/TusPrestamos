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
        
    #esta funcion era para poder filtrar los clientes por el usuario logueado pero
    #me funciono pero ya no me deja guardar los prestamos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all()
        self.fields['cliente'].widget.attrs['readonly'] = 'readonly'
    
    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['cliente'].queryset = Cliente.objects.filter(user=user)
        
class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['prestamo', 'monto_pago', 'fecha_pago']