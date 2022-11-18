from django import forms

from .models import InputModel
from django.utils.translation import gettext_lazy as _

class InputForm(forms.ModelForm):
    class Meta:
        model = InputModel
        fields = ['numAutores', 'correo','division','titulo','tipo','resumen']
        widgets = {
            'tipo': forms.RadioSelect,
            # Esto es para que solo aparezcan docx al seleccionar archivo, pero no detiene al usuario
            # de elegir otro tipo de archivo.
            'resumen': forms.FileInput(attrs={'accept':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
        }
        labels = {
            'numAutores': _('Número de autores'),
            'correo': _('Correo del representante'),
            'division': _('División o institución a la que pertenece'),
            'titulo': _('Título'),
            'tipo': _('Tipo de presentación'),
        }

class AnuncioFields(forms.Form):

    titulo = forms.CharField(label='Titulo (obligatorio)')
    cuerpo = forms.CharField(widget=forms.Textarea, label='Cuerpo (obligatorio)')
