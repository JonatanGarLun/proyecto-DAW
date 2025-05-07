import random


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

def obtener_stats_temporales(jugador):
    """
    Crea y devuelve una copia de las estadísticas del jugador,
    incluyendo buffs de pasiva y equipo.
    Esta copia se usará solo durante el combate.
    """
    stats = calcular_stats_totales(jugador)
    stats = ajuste_stats(jugador, stats)

    return {
        "salud_max": stats["salud_max"],
        "salud": stats["salud"],
        "energia_max": stats["energia_max"],
        "energia": stats["energia"],
        "ataque": stats["ataque"],
        "defensa": stats["defensa"],
        "velocidad": stats["velocidad"]
    }

# =====================
# PROBABILIDADES POR CLASE
# =====================

def tirada(probabilidad):
    return random.random() < probabilidad

def obtener_probabilidades_por_clase(clase):
    clases = {
        "GUERRERO": {
            "critico": 0.15,
            "esquivar": 0.04,
            "adicional": 0.10
        },
        "ARQUERO": {
            "critico": 0.22,
            "esquivar": 0.18,
            "adicional": 0.22
        },
        "MAGO": {
            "critico": 0.17,
            "esquivar": 0.05,
            "adicional": 0.12
        },
        "LUCHADOR": {
            "critico": 0.16,
            "esquivar": 0.07,
            "adicional": 0.14
        },
        "ESPIRITUALISTA": {
            "critico": 0.18,
            "esquivar": 0.09,
            "adicional": 0.13
        },
        "ASTRAL": {
            "critico": 0.20,
            "esquivar": 0.10,
            "adicional": 0.18
        }
    }
    return clases.get(clase.upper(), {
        "critico": 0.10,
        "esquivar": 0.05,
        "adicional": 0.10
    })

def critico(jugador):
    probabilidades = obtener_probabilidades_por_clase(jugador.clase)
    return tirada(probabilidades["critico"])

def esquivar(jugador):
    probabilidades = obtener_probabilidades_por_clase(jugador.clase)
    return tirada(probabilidades["esquivar"])

def adicional(jugador):
    probabilidades = obtener_probabilidades_por_clase(jugador.clase)
    return tirada(probabilidades["adicional"])


def accion_basica(stats_temporales, jugador):
    golpe = stats_temporales["ataque"]

    if critico(jugador):
        golpe *= 2.5
        mensaje = f"¡GOLPE CRÍTICO! Has asestado un golpe certero y causado {golpe} puntos de daño."
    else:
        mensaje = f"Has realizado un ataque básico y causado {golpe} puntos de daño."

    return golpe, mensaje


def ataque_adicional(stats, jugador):
    if adicional(jugador):
        golpe, mensaje_base = accion_basica(stats, jugador)
        mensaje_extra = f"¡Ver para creer! Gracias a su velocidad y estrategia, {jugador.nombre} ha logrado anteponerse a su rival y ataca de nuevo. "
        mensaje = f"{mensaje_extra}{mensaje_base}"
        return golpe, mensaje
    mensaje = f"El enemigo ha evitado que {jugador.nombre} continue su ataque, mala suerte"
    return 0, mensaje


def calcular_golpe_recibido(golpe, jugador, stats_temporales):
    defensa = stats_temporales["defensa"]

    if esquivar(jugador):
        mensaje = f"Gracias a la velocidad y a la estrategia de {jugador.nombre}, ha logrado evitar el ataque."
        return 0, mensaje

    danio = golpe - defensa

    salud_max = stats_temporales["salud_max"]
    umbral_minimo = max(1, int(salud_max * 0.01))

    if danio <= umbral_minimo:
        danio = umbral_minimo
        mensaje = f"{jugador.nombre} bloqueó casi todo el daño, pero aún recibe {danio} puntos de daño"

    else:
        mensaje = f"{jugador.nombre} recibe el golpe del enemigo, se ha llevado una buena y recibe {danio} puntos de daño"

    return danio, mensaje


def uso_habilidad(jugador, habilidad, stats_temporales):
    """
    Usa una habilidad activa del jugador y aplica todos sus efectos.
    Los costes y los efectos se aplican solo sobre las stats temporales.
    """
    # 🔹 Selección de habilidad
    especial = None
    if habilidad == "habilidad_1":
        especial = jugador.habilidad_1
    elif habilidad == "habilidad_2":
        especial = jugador.habilidad_2
    elif habilidad == "habilidad_3":
        especial = jugador.habilidad_3

    if not especial:
        return [], "El jugador no tiene asignada esa habilidad.", stats_temporales

    coste_energia = especial.coste_energia
    coste_salud = especial.coste_salud

    # 🔹 Verificar recursos en stats temporales
    if stats_temporales["energia"] < coste_energia:
        return [], f"No tienes suficiente energía para usar {especial.nombre}.", stats_temporales

    coste_salud_real = int(stats_temporales["salud_max"] * coste_salud)
    salud_necesaria = coste_salud_real + 1

    if stats_temporales["salud"] < salud_necesaria:
        return [], (
            f"No tienes suficiente salud para usar {especial.nombre}. "
            f"Necesitas al menos {salud_necesaria} puntos de salud."
        ), stats_temporales

    # 🔹 Descontar los costes en stats temporales
    stats_temporales["energia"] -= coste_energia
    stats_temporales["salud"] -= coste_salud_real

    # 🔹 Leer efectos
    efecto_data = especial.efecto
    efectos = efecto_data.get("efectos", [])
    mensaje_personalizado = efecto_data.get("mensaje_personalizado", "Usas una habilidad.")

    resultados = []
    mensajes = [mensaje_personalizado]

    # 🔹 Aplicar cada efecto
    for efecto in efectos:
        tipo = efecto.get("tipo")

        if tipo == "daño":
            escala = efecto.get("escala_ataque", 1)
            bonus_fijo = efecto.get("bonus_fijo", 0)
            golpe = int(stats_temporales["ataque"] * escala) + bonus_fijo
            resultados.append(("daño", golpe))
            mensajes.append(f"Causas {golpe} puntos de daño.")

        elif tipo == "curacion":
            escala = efecto.get("escala_salud", 0)
            bonus_fijo = efecto.get("bonus_fijo", 0)
            curacion = int(stats_temporales["salud_max"] * escala) + bonus_fijo
            stats_temporales["salud"] = min(
                stats_temporales["salud"] + curacion,
                stats_temporales["salud_max"]
            )
            resultados.append(("curacion", curacion))
            mensajes.append(f"Te curas {curacion} puntos de salud.")

        elif tipo == "buff":
            stat = efecto.get("stat")
            bonus = efecto.get("bonus", 0)
            duracion = efecto.get("duracion_turnos", 1)
            resultados.append(("buff", stat, bonus, duracion))
            mensajes.append(
                f"Aumentas tu {stat} en {bonus} durante {duracion} turnos."
            )

        else:
            mensajes.append("No se permitirán hechizos del mundo oscuro...")

    mensaje_final = " ".join(mensajes)
    return resultados, mensaje_final, stats_temporales


def actualizar_stats_finales(jugador, stats_temporales):
    """
    Al finalizar el combate, actualiza la salud y energía reales del jugador
    en proporción a las stats temporales finales.
    """
    porcentaje_salud = stats_temporales["salud"] / stats_temporales["salud_max"]
    porcentaje_energia = stats_temporales["energia"] / stats_temporales["energia_max"]

    nueva_salud = max(1, int(jugador.salud_maxima * porcentaje_salud))
    nueva_energia = max(0, int(jugador.energia_espiritual_maxima * porcentaje_energia))

    jugador.salud = nueva_salud
    jugador.energia_espiritual = nueva_energia
    jugador.save()