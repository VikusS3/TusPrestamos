from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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


## *TODO: crear las funcionalidades para las vistas de los prestamos y pagos
def prestamos(request):
    return render(request, 'prestamos.html')

def pagos(request):
    return render(request, 'pagos.html')