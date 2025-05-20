from math import ceil

from decorator import append
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView, FormView
from combate.enemigos import calcular_golpe_recibido_enemigo, ataque_adicional_enemigo
from combate.jugador import actualizar_stats_finales, ataque_adicional
from .forms import RegistroForm
from .models import Jugador, Combate, Enemigo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from battlebound_tactics.core.combate.jugador import (
    accion_basica,
    uso_habilidad
)
from battlebound_tactics.core.combate.efectos import (
    aplicar_estado,
    limpiar_estados_expirados
)
from battlebound_tactics.core.combate.enemigos import (
    ia_enemiga,
    usar_habilidad_enemigo,
    accion_basica_enemigo
)
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
    try:
        usuario = request.user
        jugador = get_object_or_404(Jugador, user=usuario)
        enemigo = get_object_or_404(Enemigo, id=enemigo_id)

        # Crear combate
        combate = Combate.objects.create(jugador=jugador, enemigo=enemigo)
        id_combate = combate.id
        return redirect("combate", combate_id=id_combate)
    except Jugador.DoesNotExist:
        raise Jugador.DoesNotExist(
            "Este usuario no tiene un jugador registrado. Por favor, registre un jugador primero.")


@login_required
def combate(request, combate_id):
    combate = get_object_or_404(Combate, id=combate_id)
    jugador = combate.jugador
    enemigo = combate.enemigo
    log = []
    descanso = True  # Esto nos permite curarnos cuando pasamos el turno

    if combate.terminado:
        return redirect("resultado_combate", combate_id=combate.id)

    # Comprobación de combate abandonado, retirado temporalmente
    #    if jugador.combate_abandonado and jugador.combate_abandonado_id == combate_id:
    #      jugador.combate_abandonado = False
    # jugador.combate_abandonado_id = None
    # jugador.save()

    contador = str(combate.turnos + 1)
    log.append("[Turno " + contador + "]")
    stats_jugador, stats_enemigo = inicializar_combate(request, combate)
    registrar_efecto_turno(stats_jugador, combate.jugador, log)
    registrar_efecto_turno(stats_enemigo, combate.enemigo, log)

    if stats_jugador["salud"] <= 0:
        return resolver_derrota(request, jugador, enemigo, combate, log,
                                f"💀 {jugador.nombre} ha sucumbido sido derrotado...")

    if stats_enemigo["salud"] <= 0:
        return resolver_victoria(request, jugador, enemigo, combate, log)

    if request.method == "POST":
        log.append(f"TURNO {jugador.nombre}")
        accion = request.POST.get("accion")

        # ATAQUE BÁSICO + ATAQUE ADICIONAL
        if accion == "atacar":
            descanso = True  # Recuperamos el estado de descanso
            danio, mensaje = accion_basica(stats_jugador, jugador)
            log.append(mensaje)
            danio, mensaje = calcular_golpe_recibido_enemigo(danio, enemigo, stats_enemigo)
            log.append(mensaje)
            stats_enemigo["salud"] = max(0, stats_enemigo["salud"] - danio)

            danio, mensaje = ataque_adicional(stats_jugador, jugador)
            log.append(mensaje)
            if danio != 0:
                danio, mensaje = calcular_golpe_recibido_enemigo(danio, enemigo, stats_enemigo)
                log.append(mensaje)
                stats_enemigo["salud"] = max(0, stats_enemigo["salud"] - danio)

            energia_recuperada = max(1, int(stats_jugador["energia_max"] * 0.01))
            stats_jugador["energia"] = min(stats_jugador["energia_max"], stats_jugador["energia"] + energia_recuperada)
            log.append(f"{jugador.nombre} recupera {energia_recuperada} de energía.")

        # HABILIDADES

        elif accion in ["habilidad_1", "habilidad_2", "habilidad_3"]:
            descanso = True
            resultados, mensaje = uso_habilidad(jugador, accion, stats_jugador)
            log.append(mensaje)
            for resultado in resultados:
                tipo = resultado[0]
                if tipo == "daño":
                    danio = resultado[1]
                    danio, mensaje = calcular_golpe_recibido_enemigo(danio, enemigo, stats_enemigo)
                    log.append(mensaje)
                    stats_enemigo["salud"] = max(0, stats_enemigo["salud"] - danio)
                elif tipo == "curacion":
                    curacion = resultado[1]
                    stats_jugador["salud"] = min(stats_jugador["salud_max"], stats_jugador["salud"] + curacion)
                elif tipo == "buff":
                    stat, valor, duracion = resultado[1:]
                    aplicar_estado(stats_jugador, {"tipo": "buff", "stat": stat, "valor": valor, "duracion": duracion})
                elif tipo == "debuff":
                    stat, valor, duracion = resultado[1:]
                    aplicar_estado(stats_enemigo,
                                   {"tipo": "debuff", "stat": stat, "valor": valor, "duracion": duracion})
                elif tipo == "negativo":
                    estado_nombre, valor, duracion = resultado[1:]
                    aplicar_estado(stats_enemigo,
                                   {"tipo": "negativo", "estado": estado_nombre, "valor": valor, "duracion": duracion})

        # HUIR DEL COMBATE (derrota instantánea)

        elif accion == "huir":
            actualizar_stats_finales(jugador, stats_jugador)
            return resolver_derrota(request, jugador, enemigo, combate, log)

        # PASAR EL TURNO

        elif accion == "pasar":
            log.append(f"{jugador.nombre} decide no hacer nada este turno.")

            if descanso:
                descanso = False  # Para que el jugador no abuse de la curación todos los turnos
                salud_recuperada = max(0, int(stats_jugador["salud_max"] * 0.01))
                stats_jugador["salud"] = min(stats_jugador["salud_max"], stats_jugador["salud"] + salud_recuperada)
                log.append(f" {jugador.nombre} recupera {salud_recuperada} de salud al descansar.")

        # EN CASO DE ACCIÓN NO PERMITIDA

        else:
            log.append("⚠️ Acción inválida.")

        # COMPROBAMOS SI EL JUGADOR GANA

        if stats_enemigo["salud"] <= 0:
            return resolver_victoria(request, jugador, enemigo, combate, log)

        # TURNO DEL ENEMIGO
        log.append(f"TURNO {enemigo.nombre}")

        eleccion = ia_enemiga(enemigo, stats_enemigo, stats_jugador)
        if eleccion == "basico":

            # PRIMER ATAQUE

            danio, mensaje = accion_basica_enemigo(stats_enemigo, enemigo, jugador.nivel)
            stats_jugador["salud"] = max(1, stats_jugador["salud"] - danio)
            log.append(mensaje)

            # ATAQUE ADICIONAL

            danio, mensaje = ataque_adicional_enemigo(stats_enemigo, enemigo, jugador.nivel)
            stats_jugador["salud"] = max(1, stats_jugador["salud"] - danio)
            log.append(mensaje)
        else:

            # HABILIDADES

            resultado, mensaje = usar_habilidad_enemigo(eleccion, stats_enemigo, stats_jugador, enemigo, log)
            if isinstance(resultado, int):
                stats_jugador["salud"] = max(1, stats_jugador["salud"] - resultado)
            log.append(mensaje)

        # COMPROBAMOS SI EL JUGADOR PIERDE

        if stats_jugador["salud"] <= 0:
            return resolver_derrota(request, jugador, enemigo, combate, log)

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


# Para acceder a los resultados de combate una vez terminan
@login_required
def resultado_combate(request, combate_id):
    """
    Vista final del combate, muestra al jugador el resultado del enfrentamiento.
    """
    combate = get_object_or_404(Combate, id=combate_id)

    if not combate.terminado:
        # Evita que se vea el resultado si el combate no ha concluido aún
        return redirect("combate", combate_id=combate.id)

    ganador = combate.jugador if combate.resultado == "victoria" else combate.enemigo
    perdedor = combate.enemigo if combate.resultado == "victoria" else combate.jugador

    log = request.session.pop("log_combate", ["El combate ha terminado."])

    return render(request, "app/resultado.html", {
        "combate_creado": combate,
        "ganador": ganador,
        "perdedor": perdedor,
        "log": log
    })


# @require_POST
# @csrf_exempt
# def abandonar_combate(request, combate_id):
#    combate = get_object_or_404(Combate, id=combate_id)
#    jugador = combate.jugador
#    if request.user != jugador.user:
#        return JsonResponse({"error": "Acceso denegado"}, status=403)
#    jugador.combate_abandonado = True
#    jugador.combate_abandonado_id = combate.id
#    jugador.save()
#    return JsonResponse({"status": "abandono registrado"})


# @login_required
# def verificar_abandono(request):
#    jugador = Jugador.objects.get(user=request.user)
#    if jugador.combate_abandonado:
#        return JsonResponse({"pendiente": True, "combate_id": jugador.combate_abandonado_id})
#    return JsonResponse({"pendiente": False})


# @require_POST
# @csrf_exempt
# @login_required
# def resolver_abandono(request):
#    jugador = Jugador.objects.get(user=request.user)
#    decision = request.POST.get("decision")

# combate_id = jugador.combate_abandonado_id

# if decision == "continuar":
#   jugador.combate_abandonado = False
#   jugador.combate_abandonado_id = None
#   jugador.save()
#   return JsonResponse({"continuar": True, "redirect_url": reverse("combate", args=[combate_id])})


# elif decision == "rendirse":
#   combate = get_object_or_404(Combate, id=combate_id)
#   combate.resultado = "derrota"
#   combate.terminado = True
#   combate.save()
#
#   jugador.combate_abandonado = False
#   jugador.combate_abandonado_id = None
#   jugador.save()

#   from battlebound_tactics.core.globales.session import limpiar_sesion_combate
#   limpiar_sesion_combate(request, combate.id)

#   return JsonResponse({"continuar": False, "redirect_url": reverse("resultado_combate", args=[combate_id])})

# return JsonResponse({"error": "Parámetro no válido"}, status=400)
