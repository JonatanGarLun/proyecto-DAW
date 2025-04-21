from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import RegistroForm
from .models import Jugador


# Create your views here.

#Inicio

class InicioPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la instancia de Jugador vinculada al usuario
        jugador = get_object_or_404(Jugador, user=self.request.user)

        # Ejemplo de cálculo de porcentajes de barra (ajusta a tu conveniencia)
        # Aquí asumimos que la salud, energía_espiritual y experiencia tienen un máximo fijo,
        # pero lo más común es que consultes estos valores en tu modelo o definas tu propia lógica.
        max_salud = 100
        max_energia = 100
        # Suponiendo que la experiencia para el nivel actual es de 1000 (por ejemplo)
        max_experiencia = 1000

        porcentaje_salud = (jugador.salud / max_salud) * 100 if max_salud else 0
        porcentaje_energia = (jugador.energia_espiritual / max_energia) * 100 if max_energia else 0
        porcentaje_exp = (jugador.experiencia / max_experiencia) * 100 if max_experiencia else 0

        # Opciones del carrusel
        # Puedes agregar/editar más opciones; cada opción tiene:
        # - nombre: texto que se muestra
        # - imagen: ruta de la imagen del menú (icono)
        # - url: hacia dónde navega cuando se selecciona la opción
        # - imagen_central: la imagen que se mostrará en el centro al seleccionar esta opción
        opciones = [
            {
                'nombre': 'Aventura',
                'imagen': '/static/resources/menus/aventura.png', #Imagen pequeña
                'url': '/aventura/',
                'imagen_central': '/static/resources/menus/aventura.png', #Imagen grande
            },
            {
                'nombre': 'Inventario',
                'imagen': '/static/resources/menus/inventario.png', #Imagen pequeña
                'url': '/inventario/',
                'imagen_central': '/static/resources/menus/inventario.png', #Imagen grande
            },
            {
                'nombre': 'Tienda',
                'imagen': '/static/resources/menus/tienda.png', #Imagen pequeña
                'url': '/tienda/',
                'imagen_central': '/static/resources/menus/tienda.png', #Imagen grande
            },
        ]

        context['jugador'] = jugador
        context['porcentaje_salud'] = porcentaje_salud
        context['porcentaje_energia'] = porcentaje_energia
        context['porcentaje_exp'] = porcentaje_exp
        context['opciones'] = opciones

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