from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    ## * la propiedad blacnk es para que el campo no sea obligatorio
    correo = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    #que no se pase de 0 el monto
    monto = models.DecimalField(max_digits=10, decimal_places=2 )
    fecha_prestamo = models.DateField(default=timezone.now)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plazo_dias = models.IntegerField()
    pagado = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Prestamo de {self.monto} a {self.cliente.nombre}"
    
    def fecha_vencimiento(self):
        return self.fecha_prestamo + timezone.timedelta(days=self.plazo_dias)
    
    def monto_total(self):
        return round(self.monto + (self.monto * (self.tasa_interes / 100)), 2)
    
    def cantidad_pagada(self):
        total_pagado = Pago.objects.filter(prestamo=self).aggregate(total_pagado=Sum('monto_pago'))['total_pagado'] or 0
        return total_pagado
  
    def calcular_cantidad_restante(self):
        cantidad_restante = self.total_pagar - self.cantidad_pagada()
        return cantidad_restante
    
    
    def save(self, *args, **kwargs):
        if self.tasa_interes is not None:
            tasa_decimal = self.tasa_interes / 100
            self.total_pagar = self.monto + (self.monto * tasa_decimal)
        else:
            self.total_pagar = self.monto
    
        super().save(*args, **kwargs)
    
    
    
class Pago(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Pago de {self.monto_pago} para el préstamo {self.prestamo}"