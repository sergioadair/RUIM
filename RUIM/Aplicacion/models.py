import os
from django.db import models
from time import strftime

# Create your models here.

def update_filename(instance, filename): # Método para ponerle el correo como nombre al resumen
    path = "resumenes/"+strftime("%Y")
    format = instance.correo + ".docx"
    return os.path.join(path, format)

class Anuncio(models.Model):
    Titulo = models.CharField(max_length=255)
    Cuerpo = models.TextField()
    Fecha = models.DateTimeField(auto_now_add=True)

class InputModel(models.Model):
    autores = models.TextField()
    correo = models.EmailField(max_length=250)
    division = models.CharField(max_length=250)
    titulo = models.CharField(max_length=250)
    tipo = models.CharField(max_length=250, choices=[('Platica', 'platica'), ('Poster', 'poster')], default='')
    resumen = models.FileField(upload_to=update_filename, null=True)
    asistencia = models.BooleanField(default = False)

    ESTADO_REVISION = [
        (1, 'sin revision'),
        (2, 'pendiente'),
        (3, 'aceptada'),
        (4, 'rechazada'),
    ]
    
    estado = models.IntegerField(
        choices=ESTADO_REVISION,
        default=1,
    )
    
    def __str__(self):
        return self.correo

