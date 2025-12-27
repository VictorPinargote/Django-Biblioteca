from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

#clases
    #definir los campos para la clase con sus tipos (ejm: charfield, integerfield, datefield, booleanfield, etc)
    #para tipo texto usar (models.charfied) o texto largo (models.textfield)
    #atributos de charfield:
    # max_length=n para definir la longitud maxima,
    # blank=True, null=True (para que no sean obligatorios), y sean blancos o nulos
    # unique=True (para que no se repitan)

class Autor(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=50)
    bibliografia = models.CharField(max_length=200, blank=True, null=True)
    
    # definir el nombre del objeto osea el que se va a mostrar cuando se consulte un objeto de esta clase
    def __str__(self): #definimos que sea tipo string
        return f"{self.nombre} {self.apellido}" #devolvemos el nombre y apellido del autor como nombre del objeto
    
class Libro(models.Model):
    titulo = models.CharField(max_length=20)
    #el (models.foreingkey) es para definir una llave foranea, en este caso un libro tiene un autor
    autor = models.ForeignKey(Autor,related_name="libros", on_delete=models.PROTECT)
    #related name es para definir el nombre con el que se va a acceder a los libros desde el autor
    #(on_delete)=models.PROTECT es para definir que pasa si se elimina el autor, en este caso no se puede eliminar si tiene libros asociados
    disponible = models.BooleanField(default=True) #un boolean y por defecto ponerle activado
    
    def __str__(self):
        return f"{self.titulo} - {self.autor.nombre} {self.autor.apellido}" #devolvemos el titulo del libro y el nombre del autor como nombre del objeto
    
class Prestamo(models.Model):
    # la relacion es muchos a uno, muchos prestamos pueden tener un libro
    libro = models.ForeignKey(Libro, related_name="prestamos", on_delete=models.PROTECT)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="prestamos", on_delete=models.PROTECT)
    #settins.AUTH_USER_MODEL, es para referirse al modelo de usuario que este usando el proyecto, puede ser el default o uno custom
    fecha_prestamos = models.DateField(default=timezone.now)
    #datetimefield es para fecha y hora, datefield es solo para fecha 
    fecha_max = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    
    class Meta:
        permissions = (
            ("Ver_prestamos", "Puede ver prestamos"),
            ("gestionar_prestamos", "Puede gestionar prestamos"),
        )
    
    def __str__(self):
        return f"prestamo de {self.libro} a {self.usuario}"
    
# funciones para calcular dias de retraso y multa por retraso

    #Calcular dias de retraso
    @property #con el property estamos definiendo que esta funcion se va a comportar como un atributo
    def dias_retraso(self):
        hoy = timezone.now().date() #fecha actual
        fecha_ref = self.fecha_devolucion or hoy #si la fecha de devolucion es nula se toma la fecha actual
        if fecha_ref >= self.fecha_max: #si la fecha de referencia es mayor a la fecha maxima
            return (fecha_ref - self.fecha_max).days #retorna la diferencia en dias entre la fecha de referencia y la fecha maxima
        else:
            return 0 #si no hay retraso retorna 0 dias de retraso

    #calcular multa por retraso
    @property
    def multa_retraso(self):
        tarifa = 0.50
        return self.dias_retraso * tarifa 
    #retorna la multa por retraso, multiplicando los dias de retraso por la tarifa

class Multa(models.Model):
    prestamo = models.ForeignKey(Prestamo, related_name="multas", on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=(('r', 'retraso'),
                                                    ('p', 'perdida'),
                                                    ('d','deterioro')))
    #con choices definimos las opciones que puede tener el campo tipo
    monto = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    #DecimalField se 
    pagada = models.BooleanField(default=False) #para ver si esta pagado o no pagado
    fecha = models.DateField(default=timezone.now) #fecha a la que se crea la multa ,por defecto la fecha actual

    def __str__(self):
        return f"Multa {self.tipo} - {self.monto} - {self.prestamo}"
    
    def save(self, *args, **kwargs):
        if self.tipo == 'r' and self.monto == 0:
            self.monto = self.prestamo.multa_retraso
        super().save(*args, **kwargs)

        
        #cuano yo voy al registro el monento de crear el ususario debee poder asiganarle el poder gestionar prestamos automaticamnte 

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=13)
    telefono = models.CharField(max_length=10)
    
    
    
# usar imagenes estaticas de libros 