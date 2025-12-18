from django.test import TestCase
from gestion.models import Autor, Libro


class LibroModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear un autor para usar en las pruebas
        autor = Autor.objects.create(nombre="Isaac", apellido="Asimov", bibliografia="Escritor de ciencia ficción")
        Libro.objects.create(titulo="Fundacion", autor=autor, disponible= True)
        
    def test_str_devuelve_titulo(self):
        libro = Libro.objects.get(id=1) #obtener el el id que estoy creando en setuptestdata
        self.assertEqual(str(libro), 'Fundacion')