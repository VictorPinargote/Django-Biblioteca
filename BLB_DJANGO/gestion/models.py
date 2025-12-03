from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
class Autor(models.Model): #parecido a django, 
#aca ya no necesitamos eso del guion bajo name, description nada de eso
    nombre = models.CharField(max_length=50) #models es tipo texto y tiene un maximo de caracteres de 50
    apellido = models.CharField(max_length=50) #lo mismo pero para apellido
    bibliografia = models.CharField(max_length=200, blank=True, null=True)
#HAY QUE QUE ELEGIR CUAL VA A SER EL "NAME" por asi decir, el que sea el nombre o representante de la clase o objeto. en odoo usabamos el recname
#o el display name, aca en django lo que ahcemos es lo siguiente
    def __str__(self): #por que se pone __ ?????????????????????????????????????????????????????
        return f"{self.nombre} {self.apellido}" #aca nos va a devolver como NOMBRE DEL OBJETO el nombre, espacio apellido
    
class Libro(models.Model): #clase para el libro
    titulo = models.CharField(max_length=20)
    #ACA TENEMOOS QUE HACER UNA RELACION, ACA NO HAY MANY2ONE COMO EN ODOO, ACA SE DEFINE DE UNA CON FOREIGN KEY, LO VOLVEMOS LALVE FORANEA
    autor = models.ForeignKey(Autor, related_name="libros", on_delete=models.PROTECT) #TAMBIEN DEBEMOS DEFINIR DE QUIEN ES LA LALVE FORANEA, en este caso de autor, tambien hay que
    #definir un related name
    #siempre en una foreign key hay que poner el ON DELETE, es decirle que hacer cuando alguien queira borrarlo, ya que tiene
    #relaciones y se podria romper segun lo que haga, digamos si borro el libro, los que tieenen prestado ese libro ya quedarian incompletos en su tabla
    #y se podrian romper cosas, pr eso hay que definir que hacer al borrar una llave foranea
    #el ON DELETE PROTECT lo que hace es proteger el registro apra que no sea eliminado
    #PARA QUE ES EL RELATED NAME???????????????????????????????????????????????????????????????
    #NUNCA OLVIDAR EL DEF STR
    disponible = models.BooleanField(default=True) #un boolean y por defecto viene acctivado
    def __str__(self):
        return self.titulo
    
class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, related_name="prestamos", on_delete=models.PROTECT) #llave foranea con la clase de libros, prestamo y libros
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="prestamos", on_delete=models.PROTECT)  #PARA MANEJAR USUARIOS NECESITAMOS IMPORTAR UNA LIBRERIRA, asi "from django.conf import settings" importamos
    #settins acca, necesitamos el tema del auth
    #sacamos el auth_user_model, desde donde? desde settings,
    #QUE HACE EL AUTH USER MODEL ???????????????????????????????????????????????????/
    fecha_prestamos = models.DateField(default = timezone.now) #TENEMOS QUE IMPORTAR LA LIBRERIA DE TIMEZOMNE "from django.utils import timezone"
    #para fechas hay datetime field, y el date field, uno no usa hora
    fecha_maxima = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)
    #EN DJANGO, POR DEFECTO TODOS LOS CAMPOS QUE QUEREMOS VAN A SER OBLIGATORIOS, aca no hay que poner el required = true, siempre seran obligatorios
    #si quieres que no sean obligatorios hay que poner "blank=True y null=True" asi permite registros blancos y nulos
    
    def __str__(self):
        return f"prestamo de {self.libro} a {self.usuario}" #se usan CORCHETES, aca cramos un mensaje para el nombre del objeto
    
    #AHORA VAMOS A CREAR LAS FUNCIONES PARA LA FECHA MAXIMA, MULTAS Y ASI
    #VAMOS A USAR ALGUNOS CONSTRUCTORES, ESTOS NOS PERMITEN TRABAJAR CON LAS PROPIEDADES O ATRIBUTOS DE NUESTRA CLASE
    #ES SIMILAR AL COMPUTE DE ODOO
    #QUE ES UN CONSTRUCTOR????????????????????????????????????????????

    #calcular retraso
    @property
    def dias_retraso(self):
        hoy = timezone.now().date() #el timezone now nos va a dar la fecha con zona horaria y todo, y el .date la fecha nomas
        #POR QUE USAMOS LOS 2?????????????????????????????????
        fecha_ref = self.fecha_devolucion or hoy #pondra de fecha de referencia la fecha de devolucion o la de hoy, segun cual exista, si hay la devolucion
        #no usara la de hoy, si no hay usara hoy pq va en ordeen
        if fecha_ref > self.fecha_maxima: #si la fecha de referencia es mayor a la maxima
            return (fecha_ref - self.fecha_devolucion).days #va a devolver los dias extras que se ha pasado con respeto a la fecha maxima
        #entender la logica,  pq se resta??

    #ahora la de calcular la multa
    @property
    def multa_retraso(self):
        tarifa = 0.50
        return self.dias_retraso * tarifa #multiplica los dias de retraso por la tarifa diaria para calcular
    #la funcion del dias retraso esta creando un atributo a traves de una funcion, osea a pesar de ser una funcion es un
    #atributo propio de la funcion, por eso lo podemos llamar, dias retraso se convierte en un atributo, asi que no tenemos que hacer
    #compute o meterlo dentro de otro atributo, bacansisimo

    #AHORA EL TEMA DE LA MULTA
    
class multa(models.Model):
    prestamo= models.ForeignKey(Prestamo, related_name="multas", on_delete=models.PROTECT)
    tipo = models.CharField(max_length=10, choices=(
        ('r', 'retraso'), #clave valor
        ('p', 'perdida'),
        ('d', 'deterioro')
    ))#con choices definimos las opciones que tendra, al igual que odoo se debe definir ocn una tupla
    monto = models.DecimalField(max_digits=3, decimal_places=2, default=0) #decimal field es como el float, decimal_places es para ver cuantos decimales puede tener
    pagado = models.BooleanField(default=False) #para ver si esta pagado o no pagado
    fecha = models.DateField(default=timezone.now) #fecha a la que se crea la multa ,por defecto la fecha actual

    def __str__(self):
        return f"Multa {self.tipo} - {self.monto} - {self.prestamo}"
    
    #y al igual que odoo nosotros podemos redefinir algunas fucniones
    #vamos a redefinir la funcion save
    #QUE ES REDEFINIR??????????????????????????????????????
    def save(self, *args, **kwargs): #que es args y kwgars????
        if self.tipo == 'p' and self.monto == 0:
            self.monto = self.multa_retraso
        super().save('*args **kwargs') ##QUE HACE EL SUPER??? el super como la funcion save es una funcion propia de django, y la estamso reescribiendo, el super lo que va a
        #hacer es llamar a la funcion padre, o original y ejecutarla, entonces lo que hace es que aparte de lo que definimos nosotros va a usar la funcion
        #original
        #EXPLICAR ESTA FUNCION?????????????????????????????????????????????????????????