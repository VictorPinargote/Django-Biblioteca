from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#clase para crear un formulario de registro
class RegistroUsuarioForm(UserCreationForm):
    #campos de que se llaman de el modelo User
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    #camoos que se llaama del model perfil
    cedula = forms.CharField(max_length=13, required=True)
    telefono = forms.CharField(max_length=10, required=True)

    #para elefgir la opcion de staff
    staff = forms.BooleanField(required=False)
    clave_admin = forms.CharField(max_length=25, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    