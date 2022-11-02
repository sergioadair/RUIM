from django.forms import ValidationError
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import InputForm
from .models import InputModel


# Create your views here.
def home(request):
    return HttpResponse("Home :)")


def formularioRegistro(request):
    context = {}
    context['form'] = InputForm()
    return render(request, "formularioRegistro.html", context)

def guardarFR(request):
    if request.method=='POST' and request.FILES['resumen']:
        form = InputForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES['resumen'].name.endswith('.docx'):
            form.save()
        else:
            raise ValidationError(u'Error de validación')
    return redirect('/formularioRegistro/')



@login_required(login_url="/login")
def listado(request):
    ponencias = InputModel.objects.all()
    
    return render(request, "home/listarPonencias.html", {"ponencias":ponencias})


@login_required(login_url="/login")
def seleccionPonencias(request):
    if request.method=='POST':
        seleccion = request.POST.getlist("seleccionados")
        print(seleccion)
        
        if(seleccion != []):
            ponencias = InputModel.objects.filter(id__in=seleccion)
            return render(request, "home/seleccionPonencias.html", {"ponencias":ponencias})
        
        
    return redirect('home')
    