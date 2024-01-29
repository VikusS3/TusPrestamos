from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def index(request):
    return render(request, 'index.html')

def home(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'prestamo/home.html', {'prestamos': prestamos})

def create_user(request):
    if request.method == 'GET':
        return render(request, 'prestamo/create_user.html', {'form': UserForm()})
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'prestamo/create_user.html', {'form': form})
        
        
