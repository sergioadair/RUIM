from django.contrib import admin
from .models import InputModel, Anuncio

# Register your models here.
admin.site.register(Anuncio)
admin.site.register(InputModel)