from django.urls import path

from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('home/', views.home, name='home'),
    path('prestamos/', views.prestamos, name='prestamos'),
    path('pagos/', views.pagos, name='pagos'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('clientes/', views.clientes, name='clientes'),
    path('registar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('editar_cliente/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar_cliente/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('agregar_prestamo/', views.agregar_prestamo, name='agregar_prestamo'),
    path('editar_prestamo/<int:id>/', views.editar_prestamo, name='editar_prestamo'),
    path('pagar_prestamo/<int:id>', views.pagar_prestamo, name='pagar_prestamo'),
    path('eliminar_prestamo/<int:id>/', views.eliminar_prestamo, name='eliminar_prestamo'),
]