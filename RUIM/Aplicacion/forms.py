from django import forms

from .models import InputModel
from django.utils.translation import gettext_lazy as _

class InputForm(forms.ModelForm):
    class Meta:
        model = InputModel
        fields = '__all__'
        widgets = {
            'tipo': forms.RadioSelect,
            # Esto es para que solo aparezcan docx al seleccionar archivo, pero no detiene al usuario
            # de elegir otro tipo de archivo.
            'resumen': forms.FileInput(attrs={'accept':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
        }
        labels = {
            #'seleccion': _('Selección'),
            #'descripcion': _('Descripción'),
        }
