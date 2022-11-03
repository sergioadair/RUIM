from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('Programa/', views.Programa),
    path('Poster/', views.Poster),
    path('Ubicacion/', views.Ubicacion),
    path('Registro/', views.Registro),
    path('formularioRegistro/', views.formularioRegistro),
    path('guardarFR/', views.guardarFR),
    path('login/listado', views.listado, name='listado'),
    path('login/seleccion', views.seleccionPonencias, name='seleccion'),
]