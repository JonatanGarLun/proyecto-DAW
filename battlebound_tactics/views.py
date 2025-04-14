from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import RegistroForm
from .models import Jugador


# Create your views here.

# Home
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/home.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            jugador = Jugador.objects.get(user=self.request.user)
        except Jugador.DoesNotExist:
            return redirect('registro')

        context['jugador'] = jugador
        context['opciones'] = [
            {
                'nombre': 'Aventura',
                'imagen': 'resources/imgs/aventura_icono.png',
                'url': 'aventura',
            },
            {
                'nombre': 'Inventario',
                'imagen': 'resources/imgs/inventario_icono.png',
                'url': 'inventario',
            },
            {
                'nombre': 'Tienda',
                'imagen': 'resources/imgs/tienda_icono.png',
                'url': 'tienda',
            },
            # Puedes seguir añadiendo más secciones aquí
        ]

        return context

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