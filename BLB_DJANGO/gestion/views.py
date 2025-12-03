from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Libro, Autor, Prestamo, Multa

def index(request):
    title = settings.TITLE
    
    return render(request, 'gestion/templates/home.html', {'titulo': title})

def lista_libros(request):
    pass

def crear_libro(request):
    pass

def lista_prestamo(request):
    pass

def lista_crear_prestamo(request):
    pass

def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'gestion/templates/autores.html', {'autores': autores})

def crear_autor(request):
    pass   

def lista_multas(request):
    pass

def crear_multa(request, prestamo_id):
    pass

def detalle_prestamo(request, id):
    pass


# Create your views here.

