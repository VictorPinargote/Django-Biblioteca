from django.contrib import admin
from .models import Autor
# Register your models here.

admin.site.register(Autor)  #paraa ver los autores en la pagina de adminstracion, es necesario importar el obketo o modulo tambien con
#from .models import Autor