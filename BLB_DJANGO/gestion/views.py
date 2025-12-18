from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponseForbidden
from django.contrib.auth import login

from .models import Autor, Libro, Prestamo, Multa, Perfil
from .forms import RegistroUsuarioForm

def index(request):
    titulo2 = "Hola Mundillo y sapos"
    title = settings.TITLE
    return render(request, 'gestion/templates/home.html', {'titulo': title, 't': titulo2})

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, 'gestion/templates/libros.html', {'libros': libros})

def crear_libro(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    autores = Autor.objects.all()
    if request.method == "POST": #si ya envia datos y captura en variabes para poder crear el libro
        titulo =  request.POST.get('titulo')
        autor_id =  request.POST.get('autor')
        
        if titulo and autor_id:
            autor = get_object_or_404(Autor, id=autor_id)
            Libro.objects.create(titulo=titulo, autor=autor)
            return redirect('lista_libros')
    return render(request, 'gestion/templates/crear_libros.html', {'autores': autores})

def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'gestion/templates/prestamos.html', {'prestamos': prestamos})

def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'gestion/templates/autores.html', {'autores': autores})
        
@login_required
def crear_autor(request, id=None):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if id == None:
        autor = None
        modo = 'crear'
    else:
        autor = get_object_or_404(Autor, id=id)
        modo = 'editar'
        
    if request.method == 'POST': #si ya envia datos y captura en variabes para poder crear el autor
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        bibliografia = request.POST.get('bibliografia')
        if autor == None:
            Autor.objects.create(nombre=nombre, apellido=apellido, bibliografia=bibliografia)
        else:
            autor.apellido = apellido
            autor.nombre = nombre
            autor.bibliografia = bibliografia
            autor.save()
        return redirect('lista_autores')
    context = {'autor': autor,
               'titulo': 'Editar Autor' if modo == 'editar' else 'Crear Autor',
               'texto_boton': 'Guardar cambios' if modo == 'editar' else 'Crear'}
    return render(request, 'gestion/templates/crear_autores.html', context)

def lista_multas(request):
    multas = Multa.objects.all()
    return render(request, 'multas.html', {'multas': multas})

@login_required #asegura que el usuario este logueado
def crear_prestamo(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    libro = Libro.objects.filter(disponible=True)
    usuario = User.objects.all()
    if request.method == 'POST':
        libro_id = request.POST.get('libro')
        usuario_id = request.POST.get('usuario')
        fecha_prestamo = request.POST.get('fecha_prestamo')
        fecha_max = request.POST.get('fecha_max')
        if libro_id and usuario_id and fecha_prestamo and fecha_max:
            libro = get_object_or_404(Libro, id=libro_id)
            usuario = get_object_or_404(User, id=usuario_id)
            prestamo = Prestamo.objects.create(libro = libro,
                                               usuario=usuario,
                                               fecha_prestamos=fecha_prestamo,
                                               fecha_max=fecha_max)
            libro.disponible = False
            libro.save()
            return redirect('detalle_prestamo', id=prestamo.id)
    fecha = (timezone.now().date()).isoformat() # YYYY-MM-DD este se captura l aparte de al fehc actual
    return render(request, 'gestion/templates/crear_prestamo.html', {'libros': libro,
                                                                     'usuarios': usuario,
                                                                     'fecha': fecha})

def editar_autor(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    autor = get_object_or_404(Autor, id=id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        bibliografia = request.POST.get('bibliografia')
        
        if nombre and apellido:
            autor.apellido = apellido
            autor.nombre = nombre
            autor.bibliografia = bibliografia
            autor.save()
            return redirect('lista_autores')
    
    return render(request, 'gestion/templates/editar_autor.html', {'autor': autor})

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save() #guarda el usuario en la base de datos
            cedula = form.cleaned_data.get('cedula') #obtiene el valor llamado
            telefono = form.cleaned_data.get('telefono')
            staff = form.cleaned_data.get('staff')
            clave = form.cleaned_data.get('clave_admin')
            perfil = Perfil.objects.create(usuario=usuario, cedula=cedula, telefono=telefono) #en la tabla perfil se crea columnas para el usuario, cedula y telefono
            clave_staff = "123456"
            if staff and clave == clave_staff:
                usuario.is_staff = True
                usuario.save() #guarda ese cambio en la base de datos
            login(request, usuario)
            return redirect('index')
    else:
        form = RegistroUsuarioForm() 
    return render(request, 'gestion/templates/registration/registro.html', {'form': form})

def detalle_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id=id)
    multas = prestamo.multas.all()
    return render(request, 'gestion/templates/detalle_prestamo.html', {
        'prestamo': prestamo,
        'multas': multas
    })

@login_required
def crear_multa(request, prestamo_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        monto = request.POST.get('monto', 0)
        if tipo:
            multa = Multa.objects.create(
                prestamo=prestamo,
                tipo=tipo,
                monto=monto
            )
            return redirect('detalle_prestamo', id=prestamo.id)
    return render(request, 'gestion/templates/crear_multa.html', {'prestamo': prestamo})



# Create your views here.
