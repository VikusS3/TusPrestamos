
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Cliente, Prestamo, Pago
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import F, Q
from .utils import get_random_avatar_url

# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def login_user(request):
    if request.method == 'GET':
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
    query = request.GET.get('q')
    
    clientes = Cliente.objects.filter(user=request.user)
    
    if query:
        clientes = clientes.filter(Q(nombre__icontains=query) | Q(telefono__icontains=query))
    
    context = {
        'clientes': clientes,
        'query': query,
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

            new_cliente.avatar = get_random_avatar_url()
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

    query = request.GET.get('q')
    # traer los prestamos del usuario logueado y traer el nombre del cliente
    prestamos = Prestamo.objects.select_related(
        'cliente').filter(user=request.user)

    if query:
        prestamos = prestamos.filter(
            Q(cliente__nombre__icontains=query) | Q(monto__icontains=query))

    context = {
        'prestamos': prestamos,
        'query': query
    }
    return render(request, 'prestamos.html', context)


@login_required
def agregar_prestamo(request):
    if request.method == 'GET':
        clientes = Cliente.objects.filter(user=request.user)
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


@login_required
def pagar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id, user=request.user)

    if request.method == 'POST':
        form_pago = PagoForm(request.POST)
        if form_pago.is_valid():
            monto_pago = form_pago.cleaned_data['monto_pago']
            fecha_pago = form_pago.cleaned_data['fecha_pago']
            Pago.objects.create(prestamo=prestamo,
                                monto_pago=monto_pago, fecha_pago=fecha_pago)

            Prestamo.objects.filter(id=prestamo.id).update(
                monto=F('monto') - monto_pago)

            print(prestamo.cantidad_pagada())
            print(prestamo.total_pagar)
            print(prestamo.calcular_cantidad_restante())
            if prestamo.calcular_cantidad_restante() == 0 or prestamo.calcular_cantidad_restante() < 0:
                print(prestamo.cantidad_pagada())
                print(prestamo.total_pagar)
                print(prestamo.calcular_cantidad_restante())
                Prestamo.objects.filter(id=prestamo.id).update(pagado=True)

            return redirect('prestamos')
        else:
            return render(request, 'pagar_prestamo.html', {'prestamo': prestamo, 'form_pago': form_pago})
    elif request.method == 'GET':
        form_pago = PagoForm(initial={'prestamo': prestamo})
        return render(request, 'pagar_prestamo.html', {'prestamo': prestamo, 'form_pago': form_pago})

    else:
        return render(request, 'prestamos.html', {'error': 'Error al pagar el prestamo'})


@login_required
def eliminar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id, user=request.user)
    if request.method == 'POST' or request.method == 'GET':
        prestamo.delete()
        return redirect('prestamos')


@login_required
def pagos(request):
    query = request.GET.get('q')
    pagos = Pago.objects.select_related('prestamo__cliente').all()

    if query:
        pagos = pagos.filter(Q(prestamo__cliente__nombre__icontains=query) | Q(
            monto_pago__icontains=query))

    context = {
        'pagos': pagos,
        'query': query
    }
    return render(request, 'pagos.html', context)
