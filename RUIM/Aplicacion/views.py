from django.forms import ValidationError
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageDraw, ImageFont
from django.core.mail import EmailMessage
from django.contrib import messages
from .forms import InputForm, AnuncioFields
from .models import InputModel, Anuncio
from django.conf import settings
from time import strftime


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
    if request.method=='POST' and request.FILES:
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
                tipo = request.POST['tipo'],
                resumen = request.FILES['resumen']
            )
            messages.success(request, 'El registro fue enviado con éxito.')
            
            Asunto = "Registro de ponencia enviado"
            Mensaje = "Su solicitud para participar como ponente en la RUIM "+strftime("%Y")+" ha sido enviada con éxito. Espere la confirmación en los próximos días.\n\n"
            Mensaje += "Autores: " + modelo.autores + "\n"
            Mensaje += "Correo: " + modelo.correo + "\n"
            Mensaje += "División: " + modelo.division + "\n"
            Mensaje += "Título: " + modelo.titulo + "\n"
            Mensaje += "Tipo: " + modelo.tipo + "\n"
            Emisor = settings.EMAIL_HOST_USER
            Receptor = modelo.correo
            email = EmailMessage(Asunto, Mensaje, Emisor, [Receptor])
            email.content_subtype='html'
            email.attach_file('Aplicacion/media/' + modelo.resumen.name)
            try:
                email.send()
                messages.success(request, 'La información de registro fue enviada al correo especificado.')
            except Exception:
                messages.error(request, 'No se le harán llegar al correo sus respuestas del formulario.')

            return redirect('Registro')
        else:
            messages.error(request, 'La información o el archivo que intenta enviar no son válidos. Por favor revise.')
            #print(form.data.dict())
            context = {"form": {
                'numAutores': form.cleaned_data['numAutores'], 
                'correo': form.cleaned_data['correo'], 
                'division': form.cleaned_data['division'], 
                'titulo': form.cleaned_data['titulo'], 
                'tipo': form.cleaned_data['tipo'],
                'resumen': form.cleaned_data['resumen']
            }}
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

def list_char(x):
    aux = []
    i = 0
    while i < len(x):
        if not x[i] == '\r':
            aux.append(x[i])
        i += 1
    aux2 = []
    for x in range(len(aux)):
        if aux[x] == '\n':
            aux2.append(',')
        else:
            aux2.append(aux[x])
    return aux2

def convert(s):
    new = ""
    for x in range(len(s)):
        new += s[x]
    return new

def generar_PDF(participante):
    W, H = (1280,720)
    x = participante.get().autores
    y = participante.get().tipo
    z = participante.get().titulo
    aux = convert(list_char(x))
    nombre = aux.split(",")
    num = participante.get().numAutores

    im = Image.open('Aplicacion/media/static/images/Plantilla.jpg')
    d = ImageDraw.Draw(im)
    text_color = (0, 0, 160)
    font = ImageFont.truetype("arial.ttf", 50)
    
    if num == 1:
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+352)
        d.text(location, nombre[0], fill=text_color,font=font)
    elif num == 2:
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+302)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+402)
        d.text(location, nombre[1], fill=text_color,font=font)
    elif num == 3:
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+262)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+362)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+462)
        d.text(location, nombre[2], fill=text_color,font=font)
    elif num == 4:
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+202)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+302)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+402)
        d.text(location, nombre[2], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+502)
        d.text(location, nombre[3], fill=text_color,font=font)
    elif num == 5:
        font = ImageFont.truetype("arial.ttf", 40)
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+207)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+287)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+367)
        d.text(location, nombre[2], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+447)
        d.text(location, nombre[3], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+527)
        d.text(location, nombre[4], fill=text_color,font=font)
    elif num == 6:
        font = ImageFont.truetype("arial.ttf", 37)
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+207)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+267)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+327)
        d.text(location, nombre[2], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+387)
        d.text(location, nombre[3], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+447)
        d.text(location, nombre[4], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+507)
        d.text(location, nombre[5], fill=text_color,font=font)
    elif num == 7:
        font = ImageFont.truetype("arial.ttf", 32)
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+227)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+277)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+327)
        d.text(location, nombre[2], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+377)
        d.text(location, nombre[3], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+427)
        d.text(location, nombre[4], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+477)
        d.text(location, nombre[5], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+527)
        d.text(location, nombre[6], fill=text_color,font=font)
    elif num == 8:
        font = ImageFont.truetype("arial.ttf", 30)
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+227)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+267)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+307)
        d.text(location, nombre[2], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+347)
        d.text(location, nombre[3], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+387)
        d.text(location, nombre[4], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+427)
        d.text(location, nombre[5], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+467)
        d.text(location, nombre[6], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+507)
        d.text(location, nombre[7], fill=text_color,font=font)
    elif num == 9:
        font = ImageFont.truetype("arial.ttf", 32)
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+227)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+267)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+307)
        d.text(location, nombre[2], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+347)
        d.text(location, nombre[3], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+387)
        d.text(location, nombre[4], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+427)
        d.text(location, nombre[5], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+467)
        d.text(location, nombre[6], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+507)
        d.text(location, nombre[7], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+547)
        d.text(location, nombre[8], fill=text_color,font=font)
    elif num == 10:
        font = ImageFont.truetype("arial.ttf", 32)
        w, h = d.textsize(nombre)
        location = ((W-w)/2-60, (H-h)/2+217)
        d.text(location, nombre[0], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+257)
        d.text(location, nombre[1], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+297)
        d.text(location, nombre[2], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+337)
        d.text(location, nombre[3], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+377)
        d.text(location, nombre[4], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+417)
        d.text(location, nombre[5], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+457)
        d.text(location, nombre[6], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+497)
        d.text(location, nombre[7], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+537)
        d.text(location, nombre[8], fill=text_color,font=font)
        location = ((W-w)/2-60, (H-h)/2+577)
        d.text(location, nombre[9], fill=text_color,font=font)

    font1 = ImageFont.truetype("arial.ttf", 35)
    w, h = d.textsize(nombre)
    location1 = ((W-w)/2+740, (H-h)/2+673)
    d.text(location1, y, fill=text_color,font=font1)

    w, h = d.textsize(nombre)
    location2 = ((W-w)/2-100, (H-h)/2+765)
    d.text(location2, z, fill=text_color,font=font1)

    correo = str(participante.get().correo)
    for i in range(len(correo)):
        if correo[i] == "@":
            correo_aux = correo[0:i]
    qr_code = Image.open('Aplicacion/media/static/images/'+correo_aux+'qr.png')
    b = ImageDraw.Draw(qr_code)
    text_color = (0, 0, 0)
    font = ImageFont.truetype("arial.ttf", 50)
    text = "http://127.0.0.1:8000/buscar/"
    d.text((0, 0), text, fill=text_color, font=font)
    im.paste(qr_code, (860, 1155))
    im.save("Aplicacion/certificados/certificate_"+correo_aux+".pdf")

def buscar(request):
    return render(request, "buscar.html")   

def info(request):
    if request.GET.get('usr'):
        user = request.GET.get('usr')
        users = InputModel.objects.filter(id=user)
        return render(request, "resultados.html", {"users": users, "query": user})
    else:
        mensaje = "No digitaste nada"
        return HttpResponse(mensaje)