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

        # Opciones del carrusel
        # Podemos agregar/editar más opciones; cada opción tiene:
        # - nombre: texto que se muestra
        # - imagen: ruta de la imagen del menú (imagen pequeña que aparece abajo)
        # - url: hacia dónde navega cuando se selecciona la opción
        # - imagen_central: la imagen que se mostrará en el centro al seleccionar esta opción (imagen grande que ocupa toda la pantalla)
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
            },            {
                'nombre': 'Tienda',
                'imagen': '/static/resources/menus/tienda.png', #Imagen pequeña
                'url': '/tienda/',
                'imagen_central': '/static/resources/menus/tienda.png', #Imagen grande
            },
        ]

        context['jugador'] = jugador
        context['porcentaje_salud'] = int((jugador.salud / jugador.salud_maxima) * 100)
        context['porcentaje_energia'] = int((jugador.energia_espiritual / jugador.energia_espiritual_maxima) * 100)
        context['porcentaje_exp'] = int((jugador.experiencia / jugador.experiencia_maxima) * 100)
        context['opciones'] = opciones

        return context

# Registro

class RegistroPageView(FormView):
    template_name = 'app/registro_usuario.html'
    form_class = RegistroForm
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginUserView(LoginView):
    template_name = 'registration/login.html'