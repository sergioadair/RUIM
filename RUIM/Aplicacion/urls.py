from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Programa/', views.Programa, name='Programa'),
    path('Poster/', views.Poster, name='Poster'),
    path('Ubicacion/', views.Ubicacion, name='Ubicacion'),
    path('Registro/', views.Registro, name='Registro'),
    path('Contacto/', views.Contacto, name='Contacto'),
    path('formularioRegistro/', views.formularioRegistro, name='formularioRegistro'),
    path('guardarFR/', views.guardarFR, name='guardarFR'),
    path('login/listado', views.listado, name='listado'),
    path('login/seleccion', views.seleccionPonencias, name='seleccion'),
]