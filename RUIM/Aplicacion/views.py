from django.forms import ValidationError
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import InputForm, AnuncioFields
from .models import InputModel, Anuncio
from django.conf import settings


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

def Contacto(request):
    return render(request, "home/Contacto.html")
     
def formularioRegistro(request):
    if request.method=='POST' and request.FILES.get('resumen', False):
        form = InputForm(request.POST, request.FILES)
        #post = request.POST.copy()
        #post['numAutores'] = 5
        #request.POST = post
        #print(form)
        if form.is_valid() and request.FILES['resumen'].name.endswith('.docx'):
            autores_ = ''
            for i in range(1, int(request.POST['numAutores'])+1) :
                autores_ += request.POST['autor'+str(i)]
                if i < int(request.POST['numAutores']): autores_ += ", "
            modelo = InputModel.objects.create(
                numAutores = request.POST['numAutores'],
                autores = autores_,
                correo = request.POST['correo'],
                division = request.POST['division'],
                titulo = request.POST['titulo'],
                tipo = request.POST['tipo']
            )
            messages.success(request, 'El registro fue enviado con éxito.')
            return redirect('Registro')
        else:
            messages.error(request, 'La información o el archivo que intenta enviar no son válidos. Por favor revise.')
            print(form.data.dict())
            context = {"form": InputForm(initial=form.data.dict())}
            return render(request, "formularioRegistro.html", context)
    context = {}
    context['form'] = InputForm()
    return render(request, "formularioRegistro.html", context)


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

def solicitarConstancia(request):
    return render(request, "solicitar-constancia.html")

def send_email(request):

    find_participante = InputModel.objects.filter(correo=request.POST['Email'])
    
    if not find_participante.exists():
        messages.error(request, 'La información introducida es incorrecta. Por favor revísala.')
        return redirect('/solicitar-constancia/')

    if not find_participante.get().estado == 3:
        messages.error(request, 'Participante no aceptado')
        return redirect('/solicitar-constancia/')

    generar_PDF(find_participante)
    Asunto = "Constancia digital de evento formativo"
    Mensaje = "Aquí está tu constancia digital."
    Emisor = settings.EMAIL_HOST_USER
    Receptor = request.POST['Email']
    email = EmailMessage(Asunto, Asunto, Emisor, [Receptor])
    email.content_subtype='html'
    correo = str(find_participante.get().correo)
    for i in range(len(correo)):
        if correo[i] == "@":
            correo_aux = correo[0:i]
    email.attach_file('Aplicacion/certificados/certificate_' + correo_aux + '.pdf')
    try:
        email.send()
        messages.success(request, 'La constancia fue enviada al correo especificado.')
    except Exception:
        messages.error(request, 'Se ha excedido el tiempo de espera.')
    return redirect('/solicitar-constancia/')


def generar_PDF(participante):
    W, H = (1280,720)
    nombre = participante.get().titulo

    im = Image.open('Aplicacion/media/static/images/Plantilla.jpg')
    d = ImageDraw.Draw(im)
    text_color = (0, 0, 160)
    font = ImageFont.truetype("arial.ttf", 70)

    w, h = d.textsize(nombre)
    location = ((W-w)/2, 650)
    d.text(location, nombre, fill=text_color,font=font)

    correo = str(participante.get().correo)
    for i in range(len(correo)):
        if correo[i] == "@":
            correo_aux = correo[0:i]
    qr_code = Image.open('Aplicacion/media/static/images/'+correo_aux+'qr.png')
    b = ImageDraw.Draw(qr_code)
    im.paste(qr_code, (860, 1100))
    im.save("Aplicacion/certificados/certificate_"+correo_aux+".pdf")
    