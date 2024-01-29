from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username
    
class Cliente(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tasa = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    cuotas = models.IntegerField(blank=True)
    fecha = models.DateTimeField(default=timezone.now)
    pagado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Prestamos a la persona {self.cliente.name} con un monto de {self.monto}"
    
class Pago(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(default=timezone.now)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Pago de {self.monto_pago} al prestamo {self.prestamo}"