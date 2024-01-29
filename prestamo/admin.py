from django.contrib import admin
from .models import User, Cliente, Prestamo, Pago
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'password')
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'user', 'monto', 'tasa', 'cuotas', 'fecha', 'pagado')
    
class PagoAdmin(admin.ModelAdmin):
    list_display = ('prestamo', 'fecha_pago', 'monto_pago')
    
admin.site.register(User, UserAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(Pago, PagoAdmin)
