from django.shortcuts import redirect

from battlebound_tactics.core.globales.session import limpiar_sesion_combate
from battlebound_tactics.core.combate.jugador import actualizar_stats_finales
from battlebound_tactics.core.combate.efectos import procesar_estados, limpiar_estados_expirados
from battlebound_tactics.core.globales.estadisticas import obtener_stats_temporales
from battlebound_tactics.core.combate.jugador import ganar_experiencia


def inicializar_combate(request, combate):
    """
    Carga y guarda las stats temporales de jugador y enemigo en la sesión si no están presentes.
    """
    combate_key = f"combate_{combate.id}_iniciado"
    if not request.session.get(combate_key, False):
        jugador = combate.jugador
        enemigo = combate.enemigo

        stats_jugador = obtener_stats_temporales(jugador)
        stats_enemigo = obtener_stats_temporales(enemigo)

        request.session["stats_jugador"] = stats_jugador
        request.session["stats_enemigo"] = stats_enemigo
        request.session[combate_key] = True

    return request.session["stats_jugador"], request.session["stats_enemigo"]


def registrar_efecto_turno(stats_obj, objeto, log):
    """
    Aplica efectos de estado y los registra en el log. Limpia efectos expirados.
    """
    efectos = procesar_estados(stats_obj, objeto)
    log.extend(efectos)
    limpiar_estados_expirados(stats_obj)


def resolver_victoria(request, jugador, enemigo, combate):
    """
    Procesa la victoria del jugador.
    """

    actualizar_stats_finales(jugador, request.session["stats_jugador"])

    combate.terminado = True
    combate.resultado = "victoria"
    combate.save()

    ganar_experiencia(jugador, enemigo.experiencia_otorgada)  # También está incluida la subida de nivel

    combate_id = combate.id

    limpiar_sesion_combate(request, combate_id)

    jugador.victorias += 1

    return redirect('resultado_combate', combate_id=combate_id)


def resolver_derrota(request, jugador, combate):
    """
    Procesa la derrota del jugador.
    """

    actualizar_stats_finales(jugador, request.session["stats_jugador"])

    combate.terminado = True
    combate.resultado = "derrota"
    combate.save()

    combate_id = combate.id

    limpiar_sesion_combate(request, combate_id)

    jugador.derrotas += 1

    return redirect('resultado_combate', combate_id=combate_id)
