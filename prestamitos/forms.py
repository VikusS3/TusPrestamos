from django.forms import ModelForm
from .models import Cliente, Prestamo, Pago
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import AddEmailForm


class MyCustomAddEmailForm(AddEmailForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns an allauth.account.models.EmailAddress object.
        email_address_obj = super(MyCustomAddEmailForm, self).save(request)

        # Add your own processing here.
        

        # You must return the original result.
        return email_address_obj

class CustomerCreationForm(UserCreationForm):
    first_name= forms.CharField(max_length=30, required=True, help_text='Requerido ingrese su nombre.')
    last_name=forms.CharField(max_length=50, required=True,help_text='Requerido ingrese su apellido.')
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingrese una dirección de correo electrónico válida.')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']	

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