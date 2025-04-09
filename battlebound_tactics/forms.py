from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Jugador

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    nombre = forms.CharField(max_length=100, label="Nombre de personaje")
    clase = forms.CharField(widget=forms.HiddenInput())  # Se asigna con JS desde el carrusel
    alineacion = forms.ChoiceField(
        choices=Jugador.ALINEACIONES,
        label="Alineación"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'nombre', 'clase', 'alineacion']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            # Crear el objeto Jugador asociado al usuario
            Jugador.objects.create(
                user=user,
                correo=self.cleaned_data['email'],
                nombre=self.cleaned_data['nombre'],
                clase=self.cleaned_data['clase'],
                alineacion=self.cleaned_data['alineacion']
            )

        return user
