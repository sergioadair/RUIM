import os
from django.db import models
from time import strftime
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

# Create your models here.

def update_filename(instance, filename): # Método para ponerle el correo como nombre al resumen
    path = "resumenes/"+strftime("%Y")
    format = instance.correo + ".docx"
    return os.path.join(path, format)

def numAutores_choices(): # Método para obtener un rango numérico de opciones para el select
        return [(r,r) for r in range(1, 11)]

class Anuncio(models.Model):
    Titulo = models.CharField(max_length=255)
    Cuerpo = models.TextField()
    Fecha = models.DateTimeField(auto_now_add=True)

class InputModel(models.Model):
    numAutores = models.IntegerField(choices=numAutores_choices(), default=1)
    autores = models.TextField(default='')
    correo = models.EmailField(max_length=250)
    division = models.CharField(max_length=250)
    titulo = models.CharField(max_length=250)
    tipo = models.CharField(max_length=250, choices=[('Platica', 'Plática'), ('Poster', 'Póster')], default='')
    resumen = models.FileField(upload_to=update_filename, null=True)
    asistencia = models.BooleanField(default = False)
    code = models.ImageField(blank=True)

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
    
    def save(self, *args, **kwargs):
        qr_image = qrcode.make("OTP es: "+str(self.id))
        qr_offset = Image.new('RGB', (350, 350),'white')
        qr_offset.paste(qr_image)
        correo = self.correo
        for i in range(len(correo)):
            if correo[i] == "@":
                correo_aux = correo[0:i]
        files_name = f'static/images/{correo_aux}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, 'PNG')
        self.code.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)

