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
    path('login/listado', views.listado, name='listado'),
    path('login/seleccion', views.seleccionPonencias, name='seleccion'),
    path('FormNoticias/', views.subir, name="post"),
    path('Noticias/', views.Mostrar, name="mostrar"),
    path('informe/', views.Asistencias, name="informe"),
    path('solicitar-constancia/', views.solicitarConstancia),
    path('send_email/', views.send_email),
]