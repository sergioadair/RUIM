from django.db import models
#from time import strftime

# Create your models here.

class InputModel(models.Model):
    autores = models.TextField()
    correo = models.EmailField(max_length=250)
    division = models.CharField(max_length=250)
    titulo = models.CharField(max_length=250)
    tipo = models.CharField(max_length=250, choices=[('Platica', 'platica'), ('Poster', 'poster')], default='')
    resumen = models.FileField(upload_to='resumenes/%Y', null=True)

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
