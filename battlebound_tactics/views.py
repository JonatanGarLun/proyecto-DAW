import copy
import random
from math import ceil

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, FormView
from battlebound_tactics.core.combate.enemigos import ejecutar_turno_enemigo
from battlebound_tactics.core.combate.jugador import ejecutar_turno_jugador
from battlebound_tactics.core.globales.estadisticas import generar_pasiva_aleatoria_jugador
from .forms import RegistroForm
from .models import Jugador, Combate, Enemigo, Arma, Accesorio, Activa
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from battlebound_tactics.core.combate.utils_resolvedor import (
    inicializar_combate,
    registrar_efecto_turno,
    resolver_derrota,
    resolver_victoria
)


# =================
# INICIO
# ==================

class InicioPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jugador = get_object_or_404(Jugador, user=self.request.user)

        opciones = [

            {"nombre": "Mapa", "imagen": "/static/resources/menus/mapas.png", "url": "/mapa/",
             "imagen_central": "/static/resources/menus/mapas.png"},
            {"nombre": "Fuente Sagrada", "imagen": "/static/resources/menus/fuente.png", "url": "/fuente/",
             "imagen_central": "/static/resources/menus/fuente.png"},
            {"nombre": "Equipo", "imagen": "/static/resources/menus/inventario.png", "url": "/equipo/",
             "imagen_central": "/static/resources/menus/inventario.png"},
            {"nombre": "Habilidades", "imagen": "/static/resources/menus/habilidades.png", "url": "/habilidades/",
             "imagen_central": "/static/resources/menus/habilidades.png"},
            {"nombre": "Ranking", "imagen": "/static/resources/menus/combate.png", "url": "/ranking/",
             "imagen_central": "/static/resources/menus/combate.png"}
        ]

        porcentaje_salud = ceil((jugador.salud / jugador.salud_maxima) * 100)
        porcentaje_energia = ceil((jugador.energia_espiritual / jugador.energia_espiritual_maxima) * 100)
        porcentaje_exp = ceil((jugador.experiencia / jugador.experiencia_maxima) * 100)
        if porcentaje_exp == 100:
            porcentaje_exp = 99

        context.update({
            'jugador': jugador,
            'porcentaje_salud': porcentaje_salud,
            'porcentaje_energia': porcentaje_energia,
            'porcentaje_exp': porcentaje_exp,
            'opciones': opciones
        })
        return context


# =================
# MAPA DEL MUNDO
# ==================

class MapaContinentePageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/mapa_continente.html'


# =================
# REGIÓN TRANQUILA
# ==================

class RegionPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/mapa_region.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugador'] = get_object_or_404(Jugador, user=self.request.user)
        jefe_duende = get_object_or_404(Enemigo, nombre="Gran Jefe Duende y sus Réplicas")
        enemigos = list(Enemigo.objects.exclude(dificultad__contains="Jefe"))  # Excluimos a los jefes
        enemigos_seleccionados = random.sample(enemigos, 7)
        # Enemigos elegidos al azar
        context['enemigo_bastion'] = enemigos_seleccionados[0]
        context['enemigo_dreknar'] = enemigos_seleccionados[1]
        context['enemigo_vrakk'] = enemigos_seleccionados[2]
        context['enemigo_torreon'] = enemigos_seleccionados[3]
        context['enemigo_campamento'] = enemigos_seleccionados[4]
        context['enemigo_grieta'] = enemigos_seleccionados[5]
        context['enemigo_brumuhierro'] = jefe_duende if jefe_duende else enemigos_seleccionados[6]

        return context


# =================
# REGISTRO
# ==================

class RegistroPageView(FormView):
    template_name = 'app/registro_usuario.html'
    form_class = RegistroForm
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        jugador = form.save()
        generar_pasiva_aleatoria_jugador(jugador)
        login(self.request, jugador.user)
        return super().form_valid(form)


# =================
# LOGIN
# ==================

class LoginUserView(LoginView):
    template_name = 'registration/login.html'


# =================
# RANKING
# ==================

class RankingPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/ranking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugador'] = get_object_or_404(Jugador, user=self.request.user)

        return context


# =================
# CASTILLO (FINAL)
# ==================

class CastlevyrPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/castlevyr.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jugador = get_object_or_404(Jugador, user=self.request.user)
        enemigo = get_object_or_404(Enemigo, nombre="Havva Skript")

        context["jugador"] = jugador
        context["enemigo"] = enemigo

        return context


# =================
# EQUIPAMIENTO
# ==================

@login_required
def equipamiento(request):
    usuario = request.user
    jugador = Jugador.objects.get(user=usuario)
    seleccion = request.POST.get("seleccion", None)

    if request.method == "POST":
        if 'equipar_arma_id' in request.POST:
            arma_id = request.POST['equipar_arma_id']
            arma = get_object_or_404(Arma, id=arma_id)
            if jugador.nivel >= arma.nivel_necesario:
                jugador.arma = arma
                jugador.save()
            return redirect('equipamiento')

        elif 'equipar_accesorio_id' in request.POST:
            accesorio_id = request.POST['equipar_accesorio_id']
            accesorio = get_object_or_404(Accesorio, id=accesorio_id)
            if jugador.nivel >= accesorio.nivel_necesario:
                jugador.accesorio = accesorio
                jugador.save()
            return redirect('equipamiento')

    armas = Arma.objects.all()
    accesorios = Accesorio.objects.all()

    return render(request, 'app/equipo.html', {
        'jugador': jugador,
        'armas': armas,
        'accesorios': accesorios,
        'seleccion': seleccion
    })


@login_required
def habilidades_view(request):
    usuario = request.user
    jugador = Jugador.objects.get(user=usuario)
    seleccion = request.POST.get("seleccion", None)
    habilidades = Activa.objects.all().order_by('nivel_necesario')

    if request.method == "POST":
        # Equipar habilidad en una ranura
        for i in range(1, 4):
            if f"equipar_habilidad_{i}" in request.POST:
                habilidad_id = int(request.POST[f"equipar_habilidad_{i}"])
                habilidad = get_object_or_404(Activa, id=habilidad_id)
                if jugador.nivel >= habilidad.nivel_necesario:
                    setattr(jugador, f"habilidad_{i}", habilidad)
                    jugador.save()
                return redirect('habilidades')

    return render(request, 'habilidades.html', {
        'jugador': jugador,
        'habilidades': habilidades,
        'seleccion': seleccion,
    })


# =====================
# LÓGICA DE COMBATE
# ======================

@login_required
@require_GET
def iniciar_combate(request, enemigo_id):
    jugador = get_object_or_404(Jugador, user=request.user)
    enemigo = get_object_or_404(Enemigo, id=enemigo_id)
    nombre = f"Duelo a muerte"
    combate = Combate.objects.create(nombre=nombre, jugador=jugador, enemigo=enemigo)
    return redirect("combate", combate_id=combate.id)


@login_required
def combate(request, combate_id):
    combate = get_object_or_404(Combate, id=combate_id)
    jugador = combate.jugador

    if request.user != jugador.user:
        raise PermissionDenied("No tienes permiso para acceder a este combate.")

    enemigo = combate.enemigo
    log = []

    if combate.terminado:
        return redirect("resultado_combate", combate_id=combate.id)

    # Inicializar estadísticas temporales
    stats_jugador, stats_enemigo = inicializar_combate(request, combate)

    # Para mostrar la animación de recibir un golpe
    stats_enemigo_pre_turno = copy.deepcopy(stats_enemigo)
    enemigo_herido = False
    clase_animacion_golpe = ""

    turno_actual = combate.turnos + 1
    log.append(f"[Turno {turno_actual}]")

    # Procesar estados al inicio del turno (enemigo primero para darle un poco de ventaja al jugador)
    registrar_efecto_turno(stats_enemigo, enemigo, log)
    if stats_enemigo["salud"] <= 0:
        return resolver_victoria(request, jugador, enemigo, combate)

    registrar_efecto_turno(stats_jugador, jugador, log)
    if stats_jugador["salud"] <= 0:
        return resolver_derrota(request, jugador, combate)

    # Registramos la acción del jugador
    if request.method == "POST":
        accion = request.POST.get("accion")
        if not accion:
            log.append("A los dioses no les ha gustado eso...")
            return render(request, "app/combate.html", {
                "combate_creado": combate,
                "jugador": jugador,
                "enemigo": enemigo,
                "stats_jugador": stats_jugador,
                "stats_enemigo": stats_enemigo,
                "log": log,
            })
        # Determinamos quién va primero según la velocidad velocidad
        jugador_primero = stats_jugador["velocidad"] >= stats_enemigo["velocidad"]

        if jugador_primero:
            resultado = ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion,
                                               log)  # Nuestro turno
            if resultado:  # Victoria
                return resultado
            resultado = ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log,
                                               combate)  # Turno enemigo
            if resultado:  # Derrota
                return resultado
        else:
            resultado = ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log,
                                               combate)  # Turno enemigo
            if resultado:  # Derrota
                return resultado
            resultado = ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion,
                                               log)  # Nuestro turno
            if resultado:  # Victoria
                return resultado

        # Comprobación de si el enemigo ha recibido algún daño (de cualquier tipo, incluido curaciones) para mostrar una animación
        if stats_enemigo_pre_turno["salud"] != stats_enemigo["salud"]:
            enemigo_herido = True
            clase_animacion_golpe = random.choice(
                ["animacion-golpe-1", "animacion-golpe-2", "animacion-golpe-3", "animacion-golpe-4"])

        # Guardamos las estadísticas de nuevo y avanzamos turno
        request.session["stats_jugador"] = stats_jugador
        request.session["stats_enemigo"] = stats_enemigo
        combate.turnos += 1
        combate.save()

    return render(request, "app/combate.html", {
        "combate": combate,
        "jugador": jugador,
        "enemigo": enemigo,
        "stats_jugador": stats_jugador,
        "stats_enemigo": stats_enemigo,
        "enemigo_herido": enemigo_herido,
        "clase_animacion_golpe": clase_animacion_golpe,
        "log": log
    })


def resultado_combate(request, combate_id):
    combate = get_object_or_404(Combate, id=combate_id)
    jugador = combate.jugador
    enemigo = combate.enemigo

    context = {
        "combate": combate,
        "jugador": jugador,
        "enemigo": enemigo,
    }

    return render(request, "app/resultado.html", context)


# =================
# POSADA
# ==================

def fuente(request):
    jugador = get_object_or_404(Jugador, user=request.user)
    jugador.salud = jugador.salud_maxima
    jugador.energia_espiritual = jugador.energia_espiritual_maxima
    jugador.save()
    return redirect("inicio")

# ========================================================
# Código de abandono de combate, desactivado temporalente
# =========================================================

# @require_POST
# @csrf_exempt
# def abandonar_combate(request, combate_id):
#     combate = get_object_or_404(Combate, id=combate_id)
#     jugador = combate.jugador
#     if request.user != jugador.user:
#         return JsonResponse({"error": "Acceso denegado"}, status=403)
#     jugador.combate_abandonado = True
#     jugador.combate_abandonado_id = combate.id
#     jugador.save()
#     return JsonResponse({"status": "abandono registrado"})
#
#
# @login_required
# def verificar_abandono(request):
#     jugador = Jugador.objects.get(user=request.user)
#     if jugador.combate_abandonado:
#         return JsonResponse({"pendiente": True, "combate_id": jugador.combate_abandonado_id})
#     return JsonResponse({"pendiente": False})
#
#
# @require_POST
# @csrf_exempt
# @login_required
# def resolver_abandono(request):
#     jugador = Jugador.objects.get(user=request.user)
#     decision = request.POST.get("decision")
#
#     combate_id = jugador.combate_abandonado_id
#
#     if decision == "continuar":
#         jugador.combate_abandonado = False
#         jugador.combate_abandonado_id = None
#         jugador.save()
#         return JsonResponse({"continuar": True, "redirect_url": reverse("combate", args=[combate_id])})
#
#     elif decision == "rendirse":
#         combate = get_object_or_404(Combate, id=combate_id)
#         combate.resultado = "derrota"
#         combate.terminado = True
#         combate.save()
#
#         jugador.combate_abandonado = False
#         jugador.combate_abandonado_id = None
#         jugador.save()
#
#         from battlebound_tactics.core.globales.session import limpiar_sesion_combate
#         limpiar_sesion_combate(request, combate.id)
#
#         return JsonResponse({"continuar": False, "redirect_url": reverse("resultado_combate", args=[combate_id])})
#
#     return JsonResponse({"error": "Parámetro no válido"}, status=400)
