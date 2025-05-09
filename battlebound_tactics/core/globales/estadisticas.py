def inicializar_stats(objeto):
    """
    Inicializa las estadísticas base. Compatible con Jugador y Enemigo.
    """
    stats = {
        "salud_max": objeto.salud_maxima,
        "salud": objeto.salud,
        "ataque": objeto.ataque,
        "defensa": objeto.defensa,
        "velocidad": objeto.velocidad
    }

    # Solo los jugadores tienen energía espiritual
    if hasattr(objeto, "energia_espiritual_maxima"):
        stats["energia_max"] = objeto.energia_espiritual_maxima
        stats["energia"] = objeto.energia_espiritual

    return stats


def aplicar_pasiva(jugador, stats):
    """
    Aplica bonificadores de pasiva. Solo para jugadores.
    """
    pasiva = getattr(jugador, "habilidad_pasiva", None)
    if not pasiva:
        return

    efecto = pasiva.efecto
    stats["salud_max"] += efecto.get("bonus_vida", 0)
    stats["energia_max"] += efecto.get("bonus_energia", 0)
    stats["ataque"] += efecto.get("bonus_ataque", 0)
    stats["defensa"] += efecto.get("bonus_defensa", 0)
    stats["velocidad"] += efecto.get("bonus_velocidad", 0)


def aplicar_equipo(jugador, stats):
    """
    Aplica bonificadores del arma y equipo. Solo para jugadores.
    """
    arma = getattr(jugador, "arma", None)
    equipo = getattr(jugador, "equipo", None)

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


def calcular_stats_totales(objeto):
    """
    Calcula stats base + equipo + pasiva si corresponde.
    Compatible con jugadores y enemigos.
    """
    stats = inicializar_stats(objeto)

    if hasattr(objeto, "habilidad_pasiva"):
        aplicar_pasiva(objeto, stats)

    if hasattr(objeto, "arma") or hasattr(objeto, "equipo"):
        aplicar_equipo(objeto, stats)

    return stats


def ajuste_stats(objeto, stats):
    """
    Ajusta salud y energía según proporción actual.
    """
    salud_max_antigua = objeto.salud_maxima
    salud_antigua = objeto.salud
    porcentaje_salud = salud_antigua / salud_max_antigua if salud_max_antigua else 0

    stats["salud"] = max(1, int(stats["salud_max"] * porcentaje_salud))

    if "energia_max" in stats and hasattr(objeto, "energia_espiritual_maxima"):
        energia_max_antigua = objeto.energia_espiritual_maxima
        energia_antigua = objeto.energia_espiritual
        porcentaje_energia = energia_antigua / energia_max_antigua if energia_max_antigua else 0
        stats["energia"] = max(0, int(stats["energia_max"] * porcentaje_energia))


def obtener_stats_temporales(objeto):
    """
    Calcula y devuelve stats de combate ajustadas.
    Compatible con jugadores (con energía) y enemigos (sin energía).
    """
    stats = calcular_stats_totales(objeto)
    ajuste_stats(objeto, stats)

    # Podría haber hecho estos return con un bucle for (para quitar o añadir campos), pero lo he hecho con un if para mayor simplicidad del código

    if hasattr(objeto, "energia_espiritual_maxima"):
        return {
            "salud_max": stats["salud_max"],
            "salud": stats["salud"],
            "energia_max": stats["energia_max"],
            "energia": stats["energia"],
            "ataque": stats["ataque"],
            "defensa": stats["defensa"],
            "velocidad": stats["velocidad"]
        }
    else:
        return {
            "salud_max": stats["salud_max"],
            "salud": stats["salud"],
            "ataque": stats["ataque"],
            "defensa": stats["defensa"],
            "velocidad": stats["velocidad"]
        }