from django.contrib import admin
from .models import *
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'correo')
    search_fields = ('nombre', 'telefono', 'correo')
    
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'monto', 'fecha_prestamo', 'tasa_interes', 'plazo_dias', 'pagado')
    search_fields = ('cliente__nombre', 'monto', 'fecha_prestamo', 'tasa_interes', 'plazo_dias', 'pagado')

class PagoAdmin(admin.ModelAdmin):
    list_display = ('prestamo', 'monto_pago', 'fecha_pago')
    search_fields = ('prestamo__cliente__nombre', 'monto_pago', 'fecha_pago')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Prestamo, PrestamoAdmin)
admin.site.register(Pago, PagoAdmin)