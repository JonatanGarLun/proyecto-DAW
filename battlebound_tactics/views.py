import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .core.combate.efectos import procesar_estados, limpiar_estados_expirados, aplicar_estado
from .core.combate.jugador import obtener_stats_temporales, uso_habilidad, calcular_golpe_recibido, accion_basica, actualizar_stats_finales
from .forms import RegistroForm
from .models import Jugador, Arma, Combate


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
                'nombre': 'Combate',
                'imagen': '/static/resources/menus/combate.png', #Imagen pequeña
                'url': '/combate/',
                'imagen_central': '/static/resources/menus/combate.png', #Imagen grande
            },
            {
                'nombre': 'Mapa',
                'imagen': '/static/resources/menus/mapas.png',  # Imagen pequeña
                'url': '/mapa/',
                'imagen_central': '/static/resources/menus/mapas.png',  # Imagen grande
            },
            {
                'nombre': 'Inventario',
                'imagen': '/static/resources/menus/inventario.png',  # Imagen pequeña
                'url': '/inventario/',
                'imagen_central': '/static/resources/menus/inventario.png',  # Imagen grande
            },
            {
                'nombre': 'Tienda',
                'imagen': '/static/resources/menus/tienda.png',  # Imagen pequeña
                'url': '/tienda/',
                'imagen_central': '/static/resources/menus/tienda.png',  # Imagen grande
            },
            {
                'nombre': 'Posada',
                'imagen': '/static/resources/menus/posada.png',  # Imagen pequeña
                'url': '/posada/',
                'imagen_central': '/static/resources/menus/posada.png',  # Imagen grande
            },
            {
                'nombre': 'Estadísticas',
                'imagen': '/static/resources/menus/estadisticas.png', #Imagen pequeña
                'url': '/estadísticas/',
                'imagen_central': '/static/resources/menus/estadisticas.png', #Imagen grande
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

class EstadisticasPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/registro_usuario.html'



@login_required
def combate_ejemplo(request, id_enemigo):
    #Esta view es solo un ejemplo del combate, la modificaré más adelante.
    jugador = request.user.jugador
    enemigo = get_object_or_404(Jugador, pk=id_enemigo)

    # Obtenemos stats temporales de ambos combatientes
    stats_jugador = obtener_stats_temporales(jugador)
    stats_enemigo = obtener_stats_temporales(enemigo)

    log = []

    # 1️⃣ Procesar estados al inicio del turno
    log += procesar_estados(stats_jugador, jugador)
    log += procesar_estados(stats_enemigo, enemigo)

    # 2️⃣ Eliminar estados expirados
    limpiar_estados_expirados(stats_jugador)
    limpiar_estados_expirados(stats_enemigo)

    # 3️⃣ El jugador usa una habilidad
    resultado, mensaje_habilidad = uso_habilidad(jugador, "habilidad_1", stats_jugador)
    log.append(mensaje_habilidad)

    if isinstance(resultado, tuple):
        tipo, valor = resultado

        if tipo == "daño":
            danio_recibido, mensaje_danio = calcular_golpe_recibido(valor, enemigo, stats_enemigo)
            stats_enemigo["salud"] = max(1, stats_enemigo["salud"] - danio_recibido)
            log.append(mensaje_danio)

        elif tipo == "curacion":
            stats_jugador["salud"] = min(
                stats_jugador["salud"] + valor, stats_jugador["salud_max"]
            )
            log.append(f"Recuperas {valor} puntos de salud.")

    elif isinstance(resultado, list):
        for estado in resultado:
            if estado["tipo"] == "negativo" or estado["tipo"] == "debuff":
                aplicar_estado(stats_enemigo, estado)
                log.append(f"Aplicas {estado['tipo']} al enemigo: {estado}")
            elif estado["tipo"] == "buff":
                aplicar_estado(stats_jugador, estado)
                log.append(f"Te aplicas un buff: {estado}")

    # 4️⃣ El enemigo ataca (ataque básico para este ejemplo)
    golpe, mensaje_ataque = accion_basica(stats_enemigo, enemigo)
    log.append(mensaje_ataque)

    danio_al_jugador, mensaje_danio = calcular_golpe_recibido(golpe, jugador, stats_jugador)
    stats_jugador["salud"] = max(1, stats_jugador["salud"] - danio_al_jugador)
    log.append(mensaje_danio)

    # 5️⃣ Aplicar efectos de estados expirados nuevamente
    limpiar_estados_expirados(stats_jugador)
    limpiar_estados_expirados(stats_enemigo)

    # 6️⃣ Actualizar stats reales si terminó el combate
    if stats_jugador["salud"] <= 0 or stats_enemigo["salud"] <= 0:
        actualizar_stats_finales(jugador, stats_jugador)
        actualizar_stats_finales(enemigo, stats_enemigo)
        log.append("¡El combate ha terminado!")

    return render(request, "app/combate.html", {
        "log": log,
        "stats_jugador": stats_jugador,
        "stats_enemigo": stats_enemigo
    })

