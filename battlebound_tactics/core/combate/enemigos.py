from random import choices
from globales.probabilidades import critico, adicional
from efectos import aplicar_efecto_contrario

# ============================
# FUNCIONES AUXILIARES INTERNAS
# ============================

def obtener_habilidades_disponibles(enemigo):
    return [
        h for h in [enemigo.habilidad_1, enemigo.habilidad_2, enemigo.habilidad_3]
        if h and h.esta_disponible()
    ]


# ============================
# ACCIONES DEL ENEMIGO
# ============================

def accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador):
    ataque = stats_enemigo["ataque"]
    nivel_enemigo = enemigo.nivel
    if nivel_enemigo < nivel_jugador:
        diferencia_niveles = nivel_jugador - nivel_enemigo
    else:
        diferencia_niveles = 0

    golpe = round(ataque + ((ataque * (nivel_enemigo / 100)) + (ataque * (diferencia_niveles / 100))))

    if critico(enemigo):
        golpe = int(round(golpe * 2))
        mensaje = f"{enemigo.nombre} lanza un golpe crítico que inflige {golpe} puntos de daño."
    else:
        golpe = int(round(golpe))
        mensaje = f"{enemigo.nombre} ataca y causa {golpe} puntos de daño."

    return golpe, mensaje


def ataque_adicional_enemigo(stats_enemigo, enemigo, nivel_jugador):
    """
    Intenta realizar un ataque adicional del enemigo.
    """
    if adicional(enemigo):
        golpe, mensaje_base = accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador)
        mensaje = (
            f"💥 {enemigo.nombre} aprovecha una brecha en la defensa y lanza un ataque adicional devastador."
            f"{mensaje_base}"
        )
        return golpe, mensaje

    mensaje = f"{enemigo.nombre} intenta una ofensiva rápida... pero el oponente lo anticipa y bloquea el intento."
    return 0, mensaje


# ============================
# USO DE HABILIDADES
# ============================

def usar_habilidad_enemigo(habilidad, stats_enemigo, stats_jugador, enemigo, log):
    efecto = habilidad.efecto or {}
    tipo = efecto.get("tipo")
    resultado = 0
    

    if tipo == "daño":
        escala = float(efecto.get("escala_ataque", 1.0))
        bono = int(efecto.get("valor", 0))
        resultado = int(stats_enemigo["ataque"] * escala) + bono
        mensaje = f"{enemigo.nombre} usa {habilidad.nombre} y causa {resultado} puntos de daño."

    elif tipo == "curacion":
        escala = float(efecto.get("escala_salud", 0))
        bono = int(efecto.get("valor", 0))
        resultado = int(stats_enemigo["salud_max"] * escala) + bono
        stats_enemigo["salud"] = min(stats_enemigo["salud_max"], stats_enemigo["salud"] + resultado)
        mensaje = f"{enemigo.nombre} usa {habilidad.nombre} y se cura {resultado} puntos de salud."

    elif tipo in ["buff", "debuff", "negativo"]:
        aplicar_efecto_contrario(efecto, stats_jugador, objetivo=stats_jugador["objeto"], log_combate=log)
        mensaje = f"{enemigo.nombre} lanza {habilidad.nombre} intentando aplicar un efecto de estado."

    else:
        mensaje = f"{enemigo.nombre} intenta usar {habilidad.nombre}, pero no ocurre nada."
        resultado = None

    habilidad.activar()
    habilidad.save()

    return resultado, mensaje


# ============================
# DECISIÓN DE ACCIÓN POR IA
# ============================

def ia_enemiga(enemigo, stats_enemigo, stats_jugador):
    habilidades = obtener_habilidades_disponibles(enemigo)
    opciones = []
    pesos = []

    vida_jugador = stats_jugador.get("salud", 0)
    vida_max_jugador = stats_jugador.get("salud_max", 1)
    vida_enemigo = stats_enemigo.get("salud", 0)
    vida_max_enemigo = stats_enemigo.get("salud_max", 1)

    jugador_envenenado = any(
        e["tipo"] == "negativo" and e.get("estado") == "veneno"
        for e in stats_jugador.get("estados", [])
    )

    for habilidad in habilidades:
        efecto = habilidad.efecto or {}
        tipo = efecto.get("tipo")
        peso = 1

        if tipo == "daño":
            peso = 4 if vida_jugador > vida_max_jugador * 0.5 else 2
        elif tipo == "curacion":
            peso = 5 if vida_enemigo < vida_max_enemigo * 0.4 else 1
        elif tipo == "negativo":
            peso = 3 if not jugador_envenenado else 1
        elif tipo in ["buff", "debuff"]:
            peso = 2

        opciones.append(habilidad)
        pesos.append(peso)

    opciones.append("basico")
    pesos.append(5 if not habilidades else 3)

    eleccion = choices(opciones, weights=pesos, k=1)[0]
    return eleccion


# ============================
# EJECUCIÓN COMPLETA DEL TURNO ENEMIGO
# ============================

def ejecutar_accion_enemiga(enemigo, stats_enemigo, stats_jugador, log):
    eleccion = ia_enemiga(enemigo, stats_enemigo, stats_jugador)
    nivel_jugador = stats_jugador.get("nivel", 1)

    if eleccion == "basico":
        danio, mensaje = accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador)
    else:
        danio, mensaje = usar_habilidad_enemigo(eleccion, stats_enemigo, stats_jugador, enemigo, log)

    log.append(mensaje)
    return danio
