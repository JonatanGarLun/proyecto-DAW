from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Jugador

class RegistroForm(forms.ModelForm):
    # Campos para el User
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    # Campos para Jugador (los ya existentes en el modelo)
    email = forms.EmailField(label="Correo electrónico")
    nombre = forms.CharField(label="Nombre de personaje", max_length=100)
    clase = forms.CharField(widget=forms.HiddenInput())
    alineacion = forms.ChoiceField(choices=Jugador.ALINEACIONES, label="Alineación")

    class Meta:
        model = Jugador
        fields = ['username', 'password1', 'password2', 'email', 'nombre', 'clase', 'alineacion']

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")

        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if User.objects.filter(username=cleaned_data.get("username")).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")

        if User.objects.filter(email=cleaned_data.get("email")).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")

        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.cleaned_data

        # Crear el usuario
        user = User.objects.create(
            username=cleaned_data["username"],
            password=make_password(cleaned_data["password1"]),
            email=cleaned_data["email"]
        )

        # Crear el jugador vinculado
        jugador = Jugador.objects.create(
            user=user,
            correo=cleaned_data["email"],
            nombre=cleaned_data["nombre"],
            clase=cleaned_data["clase"],
            alineacion=cleaned_data["alineacion"]
        )

        return jugador
