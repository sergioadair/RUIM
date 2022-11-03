from django.forms import ValidationError
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import InputForm, AnuncioFields
from .models import InputModel, Anuncio


# Create your views here.
def index(request):
    return render(request, "home/index.html")

def Programa(request):
    return render(request, "home/Programa.html")

def Poster(request):
    return render(request, "home/Poster.html")

def Ubicacion(request):
    return render(request, "home/Ubicacion.html")

def Registro(request):
    return render(request, "home/Registro.html")
     
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
        
        
    return redirect('listado')

@login_required(login_url="/login")
def subir(request):
    if request.method=="POST":

        Form=AnuncioFields(request.POST)

        if Form.is_valid():
            inForm=Anuncio()

            inForm.Titulo=Form.cleaned_data['titulo']
            inForm.Cuerpo=Form.cleaned_data['cuerpo']
            
            inForm.save()
            AuxForm=AnuncioFields()
            return render(request, "home/Form.html", {"form":AuxForm})
    else:
        Form=AnuncioFields()

    return render(request, "home/Form.html", {"form":Form})

def Mostrar(request):
    Anuncios = Anuncio.objects.all().order_by('-Fecha')
    return render(request, "home/Mostrar.html", {"Anuncios": Anuncios})

@login_required(login_url="/login")
def Asistencias(request):
    Ponencias = InputModel.objects.all()
    return render(request, "home/Informe.html", {"Ponencias": Ponencias})