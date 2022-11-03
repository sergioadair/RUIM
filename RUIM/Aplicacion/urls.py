from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Programa/', views.Programa, name='Programa'),
    path('Poster/', views.Poster, name='Poster'),
    path('Ubicacion/', views.Ubicacion, name='Ubicacion'),
    path('Registro/', views.Registro, name='Registro'),
    path('formularioRegistro/', views.formularioRegistro, name='formularioRegistro'),
    path('guardarFR/', views.guardarFR, name='guardarFR'),
    path('login/listado', views.listado, name='listado'),
    path('login/seleccion', views.seleccionPonencias, name='seleccion'),
    path('anuncio/', views.subir, name="post"),
    path('mostrar/', views.Mostrar, name="mostrar"),
    path('informe/', views.Asistencias, name="informe"),
]