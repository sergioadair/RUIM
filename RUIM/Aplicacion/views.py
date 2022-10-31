from django.forms import ValidationError
from django.shortcuts import redirect, render

from .forms import InputForm
import magic

# Create your views here.

"""def home(request):
    context = {}
    context['form'] = InputForm()
    return render(request, "formularioRegistro.html", context)"""

def formularioRegistro(request):
    context = {}
    context['form'] = InputForm()
    return render(request, "formularioRegistro.html", context)

def guardar(request):
    if request.method=='POST' and request.FILES['resumen']:
        form = InputForm(request.POST, request.FILES)
        # Esto es para verificar que el tipo de archivo sea docx
        tipoArchivo = magic.from_buffer(request.FILES['resumen'].read(), mime=True)
        if form.is_valid() and tipoArchivo=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            form.save()
        else:
            raise ValidationError(u'Error de validación')
    return redirect('/formularioRegistro/')