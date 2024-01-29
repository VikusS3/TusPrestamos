from django.urls import path

from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('create_user', views.create_user, name='create_user')
]