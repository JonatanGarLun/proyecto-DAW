from math import ceil
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, FormView
from battlebound_tactics.core.combate.enemigos import ejecutar_turno_enemigo
from battlebound_tactics.core.combate.jugador import ejecutar_turno_jugador
from .forms import RegistroForm
from .models import Jugador, Combate, Enemigo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from battlebound_tactics.core.combate.utils_resolvedor import (
    inicializar_combate,
    registrar_efecto_turno,
    resolver_derrota,
    resolver_victoria
)


class InicioPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jugador = get_object_or_404(Jugador, user=self.request.user)

        opciones = [
            {"nombre": "Combate", "imagen": "/static/resources/menus/combate.png", "url": "/combate/",
             "imagen_central": "/static/resources/menus/combate.png"},
            {"nombre": "Mapa", "imagen": "/static/resources/menus/mapas.png", "url": "/mapa/",
             "imagen_central": "/static/resources/menus/mapas.png"},
            {"nombre": "Inventario", "imagen": "/static/resources/menus/inventario.png", "url": "/inventario/",
             "imagen_central": "/static/resources/menus/inventario.png"},
            {"nombre": "Tienda", "imagen": "/static/resources/menus/tienda.png", "url": "/tienda/",
             "imagen_central": "/static/resources/menus/tienda.png"},
            {"nombre": "Posada", "imagen": "/static/resources/menus/posada.png", "url": "/posada/",
             "imagen_central": "/static/resources/menus/posada.png"},
            {"nombre": "Estadísticas", "imagen": "/static/resources/menus/estadisticas.png", "url": "/estadísticas/",
             "imagen_central": "/static/resources/menus/estadisticas.png"}
        ]

        context.update({
            'jugador': jugador,
            'porcentaje_salud': ceil((jugador.salud / jugador.salud_maxima) * 100),
            'porcentaje_energia': ceil((jugador.energia_espiritual / jugador.energia_espiritual_maxima) * 100),
            'porcentaje_exp': ceil((jugador.experiencia / jugador.experiencia_maxima) * 100),
            'opciones': opciones
        })
        return context


class MapaContinentePageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/mapa_continente.html'


class RegionPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/mapa_region.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugador'] = get_object_or_404(Jugador, user=self.request.user)
        context['enemigos'] = Enemigo.objects.all()
        context['prueba'] = Enemigo.objects.first()
        return context


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
@require_GET
def iniciar_combate(request, enemigo_id):
    jugador = get_object_or_404(Jugador, user=request.user)
    enemigo = get_object_or_404(Enemigo, id=enemigo_id)
    combate = Combate.objects.create(jugador=jugador, enemigo=enemigo)
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
    turno_actual = combate.turnos + 1
    log.append(f"[Turno {turno_actual}]")

    # Procesar estados al inicio del turno (enemigo primero por equilibrio)
    registrar_efecto_turno(stats_enemigo, enemigo, log)
    if stats_enemigo["salud"] <= 0:
        return resolver_victoria(request, jugador, enemigo, combate, log)

    registrar_efecto_turno(stats_jugador, jugador, log)
    if stats_jugador["salud"] <= 0:
        return resolver_derrota(request, jugador, enemigo, combate, log)

    # Acción del jugador
    if request.method == "POST":
        accion = request.POST.get("accion")
        if not accion:
            log.append("Los dioses no han permitido esa acción...")
            return render(request, "app/combate.html", {
                "combate_creado": combate,
                "jugador": jugador,
                "enemigo": enemigo,
                "stats_jugador": stats_jugador,
                "stats_enemigo": stats_enemigo,
                "log": log,
            })
        # Determinar orden según velocidad
        jugador_primero = stats_jugador["velocidad"] >= stats_enemigo["velocidad"]

        if jugador_primero:
            resultado = ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion, log)
            if resultado:  # victoria
                return resultado
            resultado = ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log, combate)
            if resultado:  # derrota
                return resultado
        else:
            resultado = ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log, combate)
            if resultado:  # derrota
                return resultado
            resultado = ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion, log)
            if resultado:  # victoria
                return resultado

        # Guardar estadísticas y avanzar turno
        request.session["stats_jugador"] = stats_jugador
        request.session["stats_enemigo"] = stats_enemigo
        combate.turnos += 1
        combate.save()

    return render(request, "app/combate.html", {
        "combate_creado": combate,
        "jugador": jugador,
        "enemigo": enemigo,
        "stats_jugador": stats_jugador,
        "stats_enemigo": stats_enemigo,
        "log": log,
    })

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
