from django.shortcuts import render
from battlebound_tactics.core.globales.session import limpiar_sesion_combate
from battlebound_tactics.core.combate.jugador import actualizar_stats_finales
from battlebound_tactics.core.combate.efectos import procesar_estados, limpiar_estados_expirados
from battlebound_tactics.core.globales.estadisticas import obtener_stats_temporales
from battlebound_tactics.core.combate.jugador import ganar_experiencia, subir_nivel


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


def resolver_victoria(request, jugador, enemigo, combate, log):
    """
    Procesa la victoria del jugador.
    """
    from battlebound_tactics.views import resultado_combate  # IMPORT PROBLEMÁTICO

    log.append(f"🎉 ¡Has derrotado a {enemigo.nombre}!")
    actualizar_stats_finales(jugador, request.session["stats_jugador"])

    combate.terminado = True
    combate.resultado = "victoria"
    combate.save()

    ganar_experiencia(jugador, enemigo.experiencia_otorgada)  # También está incluida la subida de nivel

    limpiar_sesion_combate(request, combate.id)

    return resultado_combate(request, jugador, enemigo, combate, log)


def resolver_derrota(request, jugador, enemigo, combate, log, mensaje=None):
    """
    Procesa la derrota del jugador.
    """
    from battlebound_tactics.views import resultado_combate  # IMPORT PROBLEMÁTICO

    if not mensaje:
        mensaje = f"💀 {jugador.nombre} ha sido derrotado..."
    log.append(mensaje)
    actualizar_stats_finales(jugador, request.session["stats_jugador"])

    combate.terminado = True
    combate.resultado = "derrota"
    combate.save()

    limpiar_sesion_combate(request, combate.id)

    return resultado_combate(request, jugador, enemigo, combate, log)
