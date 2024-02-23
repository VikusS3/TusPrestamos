from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cliente, Prestamo, Pago
from django.contrib.auth.decorators import login_required
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

@login_required
def my_profile(request):
    return render(request, 'my_profile.html')

@login_required
def clientes(request):
    clientes = Cliente.objects.filter(user=request.user)
    context = {
        'clientes': clientes
    }
    return render(request, 'clientes.html', context)

@login_required
def registrar_cliente(request):
    if request.method == 'GET':
        return render(request, 'registrar_cliente.html', {'form': ClienteForm()})
    else:
        try:
            form = ClienteForm(request.POST)
            new_cliente = form.save(commit=False)
            new_cliente.user = request.user
            new_cliente.save()
            return redirect('clientes')
        except ValueError:
            return render(request, 'registrar_cliente.html', {'form': ClienteForm(), 'error': 'Error al crear el cliente'})
        
@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, user=request.user)
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
    
@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id, user=request.user)
    if request.method == 'POST' or request.method == 'GET':
        cliente.delete()
        return redirect('clientes')

@login_required
def prestamos(request):
    #traer los prestamos del usuario logueado y traer el nombre del cliente
    prestamos = Prestamo.objects.select_related('cliente').filter(user=request.user)
    
    context= {
        'prestamos': prestamos
    }
    return render(request, 'prestamos.html', context)

@login_required
def agregar_prestamo(request):
    if request.method == 'GET':
        clientes= Cliente.objects.filter(user=request.user)
        return render(request, 'agregar_prestamo.html', {'form': PrestamoForm(), 'clientes': clientes})
    else:
        try:
            form = PrestamoForm(request.POST)
            prestamo = form.save(commit=False)
            prestamo.user = request.user
            prestamo.save()
            return redirect('prestamos')
        except ValueError:
            return render(request, 'agregar_prestamo.html', {'form': PrestamoForm(), 'error': 'Error al crear el prestamo'})
        
@login_required
def editar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id, user=request.user)
    print(prestamo)
    if request.method == 'GET':
        print('entro al get')
        form = PrestamoForm(instance=prestamo)
        return render(request, 'editar_prestamo.html', {'prestamo': prestamo, 'form': form})
    else:
        try:
            form = PrestamoForm(request.POST, instance=prestamo)
            form.save()
            print('prestamo editado')
            return redirect('prestamos')
        except ValueError:
            return render(request, 'editar_prestamo.html', {'prestamo': prestamo, 'form': form})

## *TODO: crear las funcionalidades para las vistas de los pagos
def pagos(request):
    ##traer los pagos y como es llave foreanea traer el nombre del cliente porque esta relacionada con 
    ##el modelo de prestamo
    pagos= Pago.objects.select_related('prestamo__cliente').all()
    
    context= {
        'pagos': pagos
    }
    return render(request, 'pagos.html', context)

