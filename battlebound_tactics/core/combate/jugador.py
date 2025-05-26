from battlebound_tactics.core.combate.utils_combate import leer_efecto
from battlebound_tactics.core.globales.probabilidades import critico, esquivar, adicional
from battlebound_tactics.core.combate.efectos import aplicar_estado


# =====================
# CÁLCULO DE ESTADÍSTICAS / ANTIGUO - Lo he modificado y lo he pasado a un módulo común para el cálculo de estadísticas
# =====================

# def inicializar_stats(jugador):
#     """
#     Inicializa las estadísticas base del jugador.
#
#     Args:
#         jugador: Objeto Jugador con atributos de estadísticas.
#
#     Returns:
#         dict: Diccionario con las estadísticas básicas.
#     """
#     stats = {
#         "salud_max": jugador.salud_maxima,
#         "salud": jugador.salud,
#         "energia_max": jugador.energia_espiritual_maxima,
#         "energia": jugador.energia_espiritual,
#         "ataque": jugador.ataque,
#         "defensa": jugador.defensa,
#         "velocidad": jugador.velocidad
#     }
#     return stats
#
#
# def aplicar_pasiva(jugador, stats):
#     """
#     Aplica los bonificadores de la habilidad pasiva del jugador a sus estadísticas.
#
#     Args:
#         jugador: Objeto Jugador con habilidad_pasiva asignada.
#         stats (dict): Estadísticas actuales.
#
#     Returns:
#         No devuelve nada.
#     """
#     pasiva = jugador.habilidad_pasiva
#     if pasiva:
#         stats["salud_max"] += pasiva.efecto.get("bonus_vida", 0)
#         stats["energia_max"] += pasiva.efecto.get("bonus_energia", 0)
#         stats["ataque"] += pasiva.efecto.get("bonus_ataque", 0)
#         stats["defensa"] += pasiva.efecto.get("bonus_defensa", 0)
#         stats["velocidad"] += pasiva.efecto.get("bonus_velocidad", 0)
#     # No hay return
#
#
# def aplicar_equipo(jugador, stats):
#     """
#     Aplica los bonificadores del arma y equipo del jugador a sus estadísticas.
#
#     Args:
#         jugador: Objeto Jugador con arma y equipo asignados.
#         stats (dict): Estadísticas actuales.
#
#     Returns:
#         No devuelve nada.
#     """
#     arma = jugador.arma
#     equipo = jugador.equipo
#     if arma:
#         stats["ataque"] += arma.ataque
#         stats["defensa"] += arma.defensa
#         stats["velocidad"] += arma.velocidad
#     if equipo:
#         stats["ataque"] += equipo.ataque
#         stats["defensa"] += equipo.defensa
#         stats["velocidad"] += equipo.velocidad
#         stats["energia_max"] += equipo.energia_espiritual_maxima
#         stats["salud_max"] += equipo.salud_maxima
#
#
# def calcular_stats_totales(jugador):
#     """
#     Calcula las estadísticas totales aplicando pasiva y equipo.
#
#     Args:
#         jugador: Objeto Jugador.
#
#     Returns:
#         dict: Estadísticas finales completas.
#     """
#     stats = inicializar_stats(jugador)
#     aplicar_pasiva(jugador, stats)
#     aplicar_equipo(jugador, stats)
#     return stats
#
#
#
# def ajuste_stats(jugador, stats):
#     """
#     Ajusta la salud y energía actuales proporcionalmente a las nuevas estadísticas máximas.
#
#     Args:
#         jugador: Objeto Jugador.
#         stats (dict): Estadísticas actuales.
#
#     Returns:
#         dict: Estadísticas ajustadas.
#     """
#     salud_max_antigua = jugador.salud_maxima
#     salud_antigua = jugador.salud
#     energia_max_antigua = jugador.energia_espiritual_maxima
#     energia_antigua = jugador.energia_espiritual
#
#     # Calculamos el porcentaje actual de salud y energía para mantener la proporción tras aplicar los nuevos máximos.
#     porcentaje_salud = salud_antigua / salud_max_antigua if salud_max_antigua else 0.0
#     porcentaje_energia = energia_antigua / energia_max_antigua if energia_max_antigua else 0.0
#
#     stats["salud"] = int(stats["salud_max"] * porcentaje_salud)
#     stats["energia"] = int(stats["energia_max"] * porcentaje_energia)
#
#     # Nos aseguramos de que la salud nunca sea menor que 1 y la energía nunca sea negativa.
#     stats["salud"] = max(1, stats["salud"])
#     stats["energia"] = max(0, stats["energia"])
#
# def obtener_stats_temporales(jugador):
#     """
#     Obtiene una copia de las estadísticas totales y ajustadas del jugador
#     que se usarán durante el combate.
#
#     Args:
#         jugador: Objeto Jugador.
#
#     Returns:
#         dict: Estadísticas temporales para el combate.
#     """
#     stats = calcular_stats_totales(jugador)
#     ajuste_stats(jugador, stats)
#
#     return {
#         "salud_max": stats["salud_max"],
#         "salud": stats["salud"],
#         "energia_max": stats["energia_max"],
#         "energia": stats["energia"],
#         "ataque": stats["ataque"],
#         "defensa": stats["defensa"],
#         "velocidad": stats["velocidad"]
#     }
#

# =====================
# ACCIONES BÁSICAS DEL COMBATE
# =====================

def accion_basica(stats_temporales, jugador):
    """
    Realiza un ataque básico, considerando posibilidad de golpe crítico.

    Args:
        stats_temporales (dict): Estadísticas actuales del jugador.
        jugador: Objeto Jugador.

    Returns:
        tuple: Daño infligido y mensaje descriptivo.
    """
    golpe = stats_temporales["ataque"]

    if critico(jugador):
        golpe = int(golpe * 2.5)
        mensaje = f"¡GOLPE CRÍTICO! Has asestado un golpe certero y causado {golpe} puntos de daño."
    else:
        mensaje = f"Has realizado un ataque básico y causado {golpe} puntos de daño."

    return golpe, mensaje


def ataque_adicional(stats, jugador):
    """
    Intenta realizar un ataque adicional (solo uno por llamada).
    """
    if adicional(jugador):
        golpe, mensaje_base = accion_basica(stats, jugador)
        mensaje = (
            f"⚡ ¡{jugador.nombre} no se rinde y se lanza con un ataque extra! {mensaje_base}"
        )
        return golpe, mensaje

    mensaje = f"🛡️ {jugador.nombre} buscó una segunda oportunidad... pero el enemigo logró frenarlo justo a tiempo."
    return 0, mensaje


def calcular_golpe_recibido(golpe, jugador, stats_temporales):
    """
    Calcula el daño recibido considerando defensa y posibilidad de esquivar.
    Aplica un daño mínimo del 1% de salud máxima.

    Args:
        golpe (int): Daño del ataque recibido.
        jugador: Objeto Jugador.
        stats_temporales (dict): Estadísticas actuales del jugador.

    Returns:
        tuple: Daño final recibido y mensaje descriptivo.
    """
    defensa = stats_temporales["defensa"]

    if esquivar(jugador):
        mensaje = f"Gracias a la velocidad y a la estrategia de {jugador.nombre}, ha logrado evitar el ataque."
        return 0, mensaje

    danio = golpe - defensa

    salud_max = stats_temporales["salud_max"]
    umbral_minimo = max(1, int(salud_max * 0.00125))

    if danio <= umbral_minimo:
        danio = umbral_minimo
        mensaje = f"{jugador.nombre} bloqueó casi todo el daño, pero aún recibe {danio} puntos de daño"

    else:
        mensaje = f"{jugador.nombre} recibe el golpe del enemigo, se ha llevado una buena y recibe {danio} puntos de daño"

    return danio, mensaje


# =====================
# USO DE HABILIDADES
# =====================

def uso_habilidad(jugador, habilidad, stats_temporales):
    """
    Usa una habilidad activa, aplicando su coste y efectos.
    Devuelve los resultados procesados y mensajes.
    """
    especial = None
    if habilidad == "habilidad_1":
        especial = jugador.habilidad_1
    elif habilidad == "habilidad_2":
        especial = jugador.habilidad_2
    elif habilidad == "habilidad_3":
        especial = jugador.habilidad_3

    if not especial:
        return [], "El jugador no tiene asignada esa habilidad."

    coste_energia = especial.coste_energia
    coste_salud = especial.coste_salud
    mensaje = leer_efecto(especial, "mensaje_personalizado", f"{jugador.nombre} usa {especial.nombre}.")

    if stats_temporales["energia"] < coste_energia:
        return [], f"No tienes suficiente energía para usar {especial.nombre}."

    coste_salud_real = int(stats_temporales["salud_max"] * coste_salud)
    if stats_temporales["salud"] < coste_salud_real + 1:
        return [], f"No tienes suficiente salud para usar {especial.nombre}."

    stats_temporales["energia"] -= coste_energia
    stats_temporales["salud"] -= coste_salud_real
    stats_temporales["energia"] = max(0, stats_temporales["energia"])
    stats_temporales["salud"] = max(1, stats_temporales["salud"])

    efecto_data = especial.efecto
    efectos = efecto_data.get("efectos", [efecto_data]) if isinstance(efecto_data, dict) else []

    resultados = []
    mensajes = [mensaje]

    for efecto in efectos:
        tipo = efecto.get("tipo")
        if tipo == "dano":
            escala = efecto.get("escala_ataque", 1)
            valor = efecto.get("valor", 0)
            golpe = stats_temporales["ataque"] + int(stats_temporales["ataque"] * escala) + valor
            resultados.append(("daño", golpe))

        elif tipo == "curacion":
            escala = efecto.get("escala_salud", 0)
            valor = efecto.get("valor", 0)
            curacion = int(stats_temporales["salud_max"] * escala) + valor
            stats_temporales["salud"] = min(stats_temporales["salud_max"], stats_temporales["salud"] + curacion)
            resultados.append(("curacion", curacion))
            mensajes.append(f"{jugador.nombre} se cura {curacion} puntos de salud.")

        elif tipo in ["buff", "debuff", "negativo"]:
            resultados.append((tipo, efecto))

        else:
            mensajes.append("No se permitiran hechizos del mundo oscuro...")

    return resultados, " ".join(mensajes)


# =====================
# CÁLCULOS POST-COMBATE
# =====================

def actualizar_stats_finales(jugador, stats_temporales):
    """
    Al finalizar el combate, actualiza la salud y energía reales del jugador
    según el porcentaje restante en las estadísticas temporales.

    Args:
        jugador: Objeto Jugador.
        stats_temporales (dict): Estadísticas actuales del combate.

    Returns:
        None
    """
    porcentaje_salud = stats_temporales["salud"] / stats_temporales["salud_max"]
    porcentaje_energia = stats_temporales["energia"] / stats_temporales["energia_max"]

    nueva_salud = max(1, int(jugador.salud_maxima * porcentaje_salud))
    nueva_energia = max(0, int(jugador.energia_espiritual_maxima * porcentaje_energia))

    jugador.salud = nueva_salud
    jugador.energia_espiritual = nueva_energia
    jugador.save()


def subir_nivel(jugador, nuevo_nivel):
    """
    Sube el jugador desde su nivel actual hasta el nuevo nivel indicado,
    aplicando escalado acumulativo en cada estadística según su clase.

    Las estadísticas que suben:
    - salud_maxima
    - energia_espiritual_maxima
    - ataque
    - defensa
    - velocidad

    El crecimiento depende de:
    - Curva base por clase.
    - Multiplicadores personalizados por stat y clase.

    :param jugador: instancia del jugador.
    :param nuevo_nivel: int, nivel al que subirá el jugador.
    """

    CURVAS_CLASE = {
        "GUERRERO": {
            "salud": 150,
            "ataque": 60,
            "defensa": 80,
            "velocidad": 12,
            "energia": 25
        },
        "ARQUERO": {
            "salud": 100,
            "ataque": 75,
            "defensa": 35,
            "velocidad": 40,
            "energia": 40
        },
        "MAGO": {
            "salud": 80,
            "ataque": 80,
            "defensa": 25,
            "velocidad": 25,
            "energia": 50
        },
        "LUCHADOR": {
            "salud": 130,
            "ataque": 65,
            "defensa": 55,
            "velocidad": 28,
            "energia": 20
        },
        "ESPIRITUALISTA": {
            "salud": 100,
            "ataque": 65,
            "defensa": 40,
            "velocidad": 30,
            "energia": 45
        },
        "ASTRAL": {
            "salud": 95,
            "ataque": 80,
            "defensa": 38,
            "velocidad": 38,
            "energia": 30
        }
    }

    MULTIPLICADORES_CLASE = {
        "GUERRERO": {
            "salud": 0.65,
            "ataque": 0.55,
            "defensa": 0.70,
            "velocidad": 0.12,
            "energia": 0.05
        },
        "ARQUERO": {
            "salud": 0.35,
            "ataque": 0.40,
            "defensa": 0.28,
            "velocidad": 0.40,
            "energia": 0.07
        },
        "MAGO": {
            "salud": 0.35,
            "ataque": 0.50,
            "defensa": 0.20,
            "velocidad": 0.25,
            "energia": 0.20
        },
        "LUCHADOR": {
            "salud": 0.60,
            "ataque": 0.64,
            "defensa": 0.40,
            "velocidad": 0.20,
            "energia": 0.06
        },
        "ESPIRITUALISTA": {
            "salud": 0.35,
            "ataque": 0.65,
            "defensa": 0.40,
            "velocidad": 0.20,
            "energia": 0.10
        },
        "ASTRAL": {
            "salud": 0.28,
            "ataque": 0.56,
            "defensa": 0.35,
            "velocidad": 0.20,
            "energia": 0.1
        }
    }

    clase = jugador.clase.upper()
    curva = CURVAS_CLASE.get(clase)
    multiplicadores = MULTIPLICADORES_CLASE.get(clase)

    if not curva or not multiplicadores:
        raise ValueError(f"La clase {clase} no tiene definidas curvas o multiplicadores.")

    salud = jugador.salud_maxima
    energia = jugador.energia_espiritual_maxima
    ataque = jugador.ataque
    defensa = jugador.defensa
    velocidad = jugador.velocidad

    nivel_actual = getattr(jugador, "nivel", 1)

    if nuevo_nivel <= nivel_actual:
        raise ValueError("Nuevo nivel debe ser superior al nivel actual.")

    # Aplicamos las mejoras para cada nivel nuevo (sin repetir el nivel actual). El +1 es necesario porque range excluye el límite superior.
    for nivel in range(nivel_actual + 1, nuevo_nivel + 1):
        salud += int(curva["salud"] * (1 + nivel * multiplicadores["salud"] + (nivel * 0.25)))
        energia += int(curva["energia"] * (1 + nivel * multiplicadores["energia"] + (nivel * 0.25)))
        ataque += int(curva["ataque"] * (1 + nivel * multiplicadores["ataque"] + (nivel * 0.25)))
        defensa += int(curva["defensa"] * (1 + nivel * multiplicadores["defensa"] + (nivel * 0.25)))
        velocidad += int(curva["velocidad"] * (1 + nivel * multiplicadores["velocidad"] + (nivel * 0.25)))

    jugador.salud_maxima = salud
    jugador.energia_espiritual_maxima = energia
    jugador.ataque = ataque
    jugador.defensa = defensa
    jugador.velocidad = velocidad
    jugador.nivel = nuevo_nivel

    jugador.salud = salud
    jugador.energia_espiritual = energia

    jugador.save()


def obtener_incremento_exp_por_nivel(nivel):
    if nivel <= 25:
        return 0.05
    elif nivel <= 50:
        return 0.08
    elif nivel <= 80:
        return 0.12
    elif nivel <= 120:
        return 0.15
    else:
        return 0.20


def ganar_experiencia(jugador, exp_ganada):
    """
    Suma experiencia al jugador. Si alcanza el máximo, sube de nivel
    y aumenta la experiencia necesaria para el siguiente nivel.
    """

    log = []
    jugador.experiencia += exp_ganada
    log.append(f"Has ganado {exp_ganada} puntos de experiencia.")

    while jugador.experiencia >= jugador.experiencia_maxima:
        jugador.experiencia -= jugador.experiencia_maxima

        nivel_anterior = jugador.nivel
        nuevo_nivel = jugador.nivel + 1

        subir_nivel(jugador, nuevo_nivel)

        log.append(
            f"¡Subiste de nivel! Nivel {nivel_anterior} ➜ {nuevo_nivel}."
        )

        porcentaje_escalado = obtener_incremento_exp_por_nivel(jugador.nivel)

        # Incrementamos la experiencia máxima requerida para el siguiente nivel según el porcentaje que depende del nivel actual.
        jugador.experiencia_maxima = int(
            jugador.experiencia_maxima * (1 + porcentaje_escalado)
        )

    log.append(
        f"Ahora necesitas {jugador.experiencia_maxima} puntos de experiencia para el próximo nivel."
    )

    jugador.save()

    return log

# =====================
# TURNO DEL JUGADOR
# =====================

def ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion, log):
    from battlebound_tactics.core.combate.enemigos import calcular_golpe_recibido_enemigo # IMPORT PROBLEMÁTICO
    from battlebound_tactics.core.combate.utils_resolvedor import resolver_derrota, resolver_victoria # IMPORT PROBLEMÁTICO

    if accion == "atacar":
        danio, mensaje = accion_basica(stats_jugador, jugador)
        log.append(mensaje)
        danio, mensaje = calcular_golpe_recibido_enemigo(danio, enemigo, stats_enemigo)
        log.append(mensaje)
        stats_enemigo["salud"] = max(0, stats_enemigo["salud"] - danio)

        danio, mensaje = ataque_adicional(stats_jugador, jugador)
        log.append(mensaje)
        if danio > 0:
            danio, mensaje = calcular_golpe_recibido_enemigo(danio, enemigo, stats_enemigo)
            log.append(mensaje)
            stats_enemigo["salud"] = max(0, stats_enemigo["salud"] - danio)

        energia_recuperada = max(1, int(stats_jugador["energia_max"] * 0.01))
        stats_jugador["energia"] = min(stats_jugador["energia_max"], stats_jugador["energia"] + energia_recuperada)
        log.append(f"{jugador.nombre} recupera {energia_recuperada} de energía.")

    elif accion in ["habilidad_1", "habilidad_2", "habilidad_3"]:
        resultados, mensaje = uso_habilidad(jugador, accion, stats_jugador)
        log.append(mensaje)
        for tipo, dato in resultados:
            if tipo == "daño":
                danio = dato
                danio, mensaje = calcular_golpe_recibido_enemigo(danio, enemigo, stats_enemigo)
                log.append(mensaje)
                stats_enemigo["salud"] = max(0, stats_enemigo["salud"] - danio)
            elif tipo in ["buff", "debuff", "negativo"]:
                objetivo = stats_jugador if tipo == "buff" else stats_enemigo
                aplicar_estado(objetivo, dato)

    elif accion == "huir":
        actualizar_stats_finales(jugador, stats_jugador)
        return resolver_derrota(request, jugador, combate, log, f"{jugador.nombre} ha huido del combate.")

    elif accion == "pasar":
        log.append(f"{jugador.nombre} decide no hacer nada este turno.")
        salud_recuperada = max(0, int(stats_jugador["salud_max"] * 0.01))
        stats_jugador["salud"] = min(stats_jugador["salud_max"], stats_jugador["salud"] + salud_recuperada)
        log.append(f"{jugador.nombre} recupera {salud_recuperada} de salud al descansar.")

    else:
        log.append("⚠️ Acción inválida.")

    if stats_enemigo["salud"] <= 0:
        return resolver_victoria(request, jugador, enemigo, combate, log)

    return None

