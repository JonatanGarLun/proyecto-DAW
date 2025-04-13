from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import RegistroForm
from .models import Jugador


# Create your views here.

# Home
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/home.html'
#    redirect_field_name = 'next'

# Registro

class RegistroPageView(FormView):
    template_name = 'app/registro_usuario.html'
    form_class = RegistroForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginUserView(LoginView):
    template_name = 'registration/login.html'