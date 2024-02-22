from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cliente, Prestamo, Pago
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method=='GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'El usuario no existe'
            })
        else:
            login(request, user)
            return redirect('home')
        

def registrar_usuario(request):
    if request.method == 'GET':
        return render(request, 'registrar_usuario.html', {'form': UserCreationForm})
    
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'registrar_usuario.html', {'form': UserCreationForm, 'error': 'El usuario ya existe'})
        else:
            return render(request, 'registrar_usuario.html', {'form': UserCreationForm, 'error': 'Las contraseñas no coinciden'})

def cerrar_sesion(request):
    logout(request)
    return redirect('index')


def my_profile(request):
    return render(request, 'my_profile.html')

def clientes(request):
    clients= Cliente.objects.all()
    return render(request, 'clientes.html', {'clients': clients})

def registrar_cliente(request):
    if request.method == 'GET':
        return render(request, 'registrar_cliente.html', {'form': ClienteForm()})
    else:
        try:
            form = ClienteForm(request.POST)
            form.save()
            return redirect('clientes')
        except ValueError:
            return render(request, 'registrar_cliente.html', {'form': ClienteForm(), 'error': 'Error al crear el cliente'})
        
        
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'GET':
        form = ClienteForm(instance=cliente)
        return render(request, 'editar_cliente.html', {'cliente': cliente, 'form': form})
    else:
        try:
            form = ClienteForm(request.POST, instance=cliente)
            form.save()
            return redirect('clientes')
        except ValueError:
            return render(request, 'editar_cliente.html', {'cliente': cliente, 'form': form, 'error': 'Error al editar el cliente'})
        
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST' or request.method == 'GET':
        cliente.delete()
        return redirect('clientes')

## *TODO: crear las funcionalidades para las vistas de los prestamos y pagos
def prestamos(request):
    prestamos= Prestamo.objects.all()
    return render(request, 'prestamos.html',{'prestamos': prestamos})

def pagos(request):
    ##traer los pagos y como es llave foreanea traer el nombre del cliente porque esta relacionada con 
    ##el modelo de prestamo
    pagos= Pago.objects.select_related('prestamo__cliente').all()
    
    context= {
        'pagos': pagos
    }
    return render(request, 'pagos.html', context)

