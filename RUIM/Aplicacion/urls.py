from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('formularioRegistro/', views.formularioRegistro),
    path('guardarFR/', views.guardarFR),
    
    path('login/listado', views.listado, name='listado'),
    path('login/seleccion', views.seleccionPonencias, name='seleccion'),
]