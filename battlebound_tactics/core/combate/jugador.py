import random
from random import randint


def inicializar_stats(jugador):
    stats = {
        "salud_max": jugador.salud_maxima,
        "salud": jugador.salud,
        "energia_max": jugador.energia_espiritual_maxima,
        "energia": jugador.energia_espiritual,
        "ataque": jugador.ataque,
        "defensa": jugador.defensa,
        "velocidad": jugador.velocidad
    }
    return stats


def aplicar_pasiva(jugador, stats):
    pasiva = jugador.habilidad_pasiva
    if pasiva:
        stats["salud_max"] += pasiva.efecto.get("bonus_vida", 0)
        stats["energia_max"] += pasiva.efecto.get("bonus_energia", 0)
        stats["ataque"] += pasiva.efecto.get("bonus_ataque", 0)
        stats["defensa"] += pasiva.efecto.get("bonus_defensa", 0)
        stats["velocidad"] += pasiva.efecto.get("bonus_velocidad", 0)
    return stats


def aplicar_equipo(jugador, stats):
    arma = jugador.arma if jugador.arma else None
    equipo = jugador.equipo if jugador.equipo else None
    if arma:
        stats["ataque"] += arma.ataque
        stats["defensa"] += arma.defensa
        stats["velocidad"] += arma.velocidad
    if equipo:
        stats["ataque"] += equipo.ataque
        stats["defensa"] += equipo.defensa
        stats["velocidad"] += equipo.velocidad
        stats["energia_max"] += equipo.energia_espiritual_maxima
        stats["salud_max"] += equipo.salud_maxima
    return stats


def calcular_stats_totales(jugador):
    stats = inicializar_stats(jugador)
    stats = aplicar_pasiva(jugador, stats)
    stats = aplicar_equipo(jugador, stats)
    return stats


def ajuste_stats(jugador, stats):
    salud_max_antigua = jugador.salud_maxima
    salud_antigua = jugador.salud
    energia_max_antigua = jugador.energia_espiritual_maxima
    energia_antigua = jugador.energia_espiritual

    # Calculamos porcentaje actual
    porcentaje_salud = salud_antigua / salud_max_antigua if salud_max_antigua else 1
    porcentaje_energia = energia_antigua / energia_max_antigua if energia_max_antigua else 1

    # Aplicamos los porcentajes a las nuevas máximas
    stats["salud"] = int(stats["salud_max"] * porcentaje_salud)
    stats["energia"] = int(stats["energia_max"] * porcentaje_energia)

    return stats


def _probabilidades():
    return random.randint(1, 10) == 1


def accion_basica(jugador):
    stats = calcular_stats_totales(jugador)
    golpe = stats["ataque"]
    if _probabilidades():
        golpe *= 2
        mensaje = f"¡GOLPE CRÍTICO, has acertado un golpe certero y le has causado {golpe} puntos de daño!"
    else:
        mensaje = f"¡Has realizado un ataque básico contra el enemigo! Le has causado {golpe} puntos de daño"

    return golpe, mensaje


def ataque_adicional(jugador):
    if _probabilidades():
        mensaje = f"¡Ver para creer! Gracias a su velocidad y estrategia, {jugador.nombre} ha logrado anteponerse a su rival y ataca de nuevo"
        return accion_basica(jugador), mensaje
    mensaje = f"El enemigo ha evitado que {jugador.nombre} continue su ataque, mala suerte"
    return -1, mensaje


def calcular_golpe_recibido(golpe, jugador):
    stats = calcular_stats_totales(jugador)
    defensa = stats["defensa"]
    if _probabilidades():
        mensaje = f"{jugador.nombre} ha logrado leer a su enemigo y evitar su ataque, ¡buenos reflejos!"
        return 0, mensaje

    danio = golpe - defensa
    mensaje = f"{jugador.nombre} recibe el golpe del enemigo, se ha llevado una buena y recibe {golpe} de daño"

    if danio <= 0:

        if golpe < 100:
            danio = 1

        if 100 <= golpe < 999:
            danio = 2

        if 999 <= golpe < 10000:
            danio = randint(1, 10)
        if 10000 <= golpe < 100000:
            danio = random.randint(10, 50)
        if golpe >= 100000:
            danio = random.randint(1, 200)

        mensaje = f"{jugador.nombre} ha encajado el golpe del enemigo y recibe {danio} puntos de daño"

    return danio, mensaje
