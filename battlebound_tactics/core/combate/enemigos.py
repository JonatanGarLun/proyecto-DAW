from random import choices
from battlebound_tactics.core.combate.utils_combate import leer_efecto
from battlebound_tactics.core.globales.probabilidades import critico, adicional
from battlebound_tactics.core.combate.efectos import aplicar_efecto_contrario


# ============================
# FUNCIONES AUXILIARES INTERNAS
# ============================

def obtener_habilidades_disponibles(enemigo):
    return [
        h for h in enemigo.habilidades_asignadas.all()
        if h.preparada()
    ]


def evaluar_buff_o_debuff(tipo, stat_objetivo, stats_enemigo, stats_jugador):
    ataque_e = stats_enemigo.get("ataque", 0)
    defensa_e = stats_enemigo.get("defensa", 0)
    velocidad_e = stats_enemigo.get("velocidad", 0)

    ataque_j = stats_jugador.get("ataque", 0)
    defensa_j = stats_jugador.get("defensa", 0)
    velocidad_j = stats_jugador.get("velocidad", 0)

    if tipo == "buff":
        if stat_objetivo == "ataque" and ataque_e < defensa_j:
            return 4
        elif stat_objetivo == "defensa" and defensa_e < ataque_j:
            return 4
        elif stat_objetivo == "velocidad" and velocidad_e < velocidad_j:
            return 4
        return 2

    elif tipo == "debuff":
        if stat_objetivo == "defensa" and ataque_e < defensa_j:
            return 4
        elif stat_objetivo == "ataque" and defensa_e < ataque_j:
            return 4
        elif stat_objetivo == "velocidad" and velocidad_e < velocidad_j:
            return 4
        return 2

    return 1


# ============================
# ACCIONES BÁSICAS
# ============================

def accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador):
    ataque = stats_enemigo["ataque"]
    nivel_enemigo = enemigo.nivel
    diferencia_niveles = nivel_jugador - nivel_enemigo if nivel_enemigo < nivel_jugador else 0

    golpe = round(ataque + ((ataque * (nivel_enemigo / 100)) + (ataque * (diferencia_niveles / 100))))

    if critico(enemigo):
        golpe = int(round(golpe * 2))
        mensaje = f"{enemigo.nombre} lanza un golpe crítico que inflige {golpe} puntos de daño."
    else:
        golpe = int(round(golpe))
        mensaje = f"{enemigo.nombre} ataca y causa {golpe} puntos de daño."

    return golpe, mensaje


def ataque_adicional_enemigo(stats_enemigo, enemigo, nivel_jugador):
    if adicional(enemigo):
        golpe, mensaje_base = accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador)
        mensaje = (
            f"💥 {enemigo.nombre} aprovecha una brecha en la defensa y lanza un ataque adicional devastador. "
            f"{mensaje_base}"
        )
        return golpe, mensaje

    mensaje = f"{enemigo.nombre} intenta una ofensiva rápida... pero el oponente lo anticipa y bloquea el intento."
    return 0, mensaje


# ============================
# USO DE HABILIDADES
# ============================

def usar_habilidad_enemigo(habilidad, stats_enemigo, stats_jugador, enemigo, log):
    tipo = str(leer_efecto(habilidad, "tipo", "")).lower()
    cooldown = leer_efecto(habilidad, "cooldown", 1)

    resultado = 0
    mensaje = ""

    if tipo == "daño":
        escala = float(leer_efecto(habilidad, "escala_ataque", 1.0))
        bono = int(leer_efecto(habilidad, "valor", 0))
        resultado = int(stats_enemigo["ataque"] * escala) + bono
        mensaje = f"{enemigo.nombre} usa {habilidad.plantilla.nombre} y causa {resultado} puntos de daño."

    elif tipo == "curacion":
        escala = float(leer_efecto(habilidad, "escala_salud", 0.0))
        bono = int(leer_efecto(habilidad, "valor", 0))
        resultado = int(stats_enemigo["salud_max"] * escala) + bono
        stats_enemigo["salud"] = min(stats_enemigo["salud_max"], stats_enemigo["salud"] + resultado)
        mensaje = f"{enemigo.nombre} usa {habilidad.plantilla.nombre} y se cura {resultado} puntos de salud."

    elif tipo in ["buff", "debuff", "negativo"]:
        efecto = {
            "tipo": tipo,
            "estado": leer_efecto(habilidad, "estado"),
            "stat": leer_efecto(habilidad, "stat"),
            "valor": leer_efecto(habilidad, "valor", 0),
            "duracion": leer_efecto(habilidad, "duracion", 1),
            "porcentaje": leer_efecto(habilidad, "porcentaje", False),
            "probabilidad": leer_efecto(habilidad, "probabilidad", 1.0),
        }
        aplicar_efecto_contrario(efecto, stats_jugador, objetivo=stats_jugador["objeto"], log_combate=log)
        mensaje = f"{enemigo.nombre} lanza {habilidad.plantilla.nombre} e intenta alterar el curso del combate."

    else:
        mensaje = f"{enemigo.nombre} intenta usar {habilidad.plantilla.nombre}, pero no ocurre nada."
        resultado = None

    habilidad.activar(cooldown)
    habilidad.save()

    return resultado, mensaje


# ============================
# IA DEL ENEMIGO
# ============================

def ia_enemiga(enemigo, stats_enemigo, stats_jugador):
    habilidades = obtener_habilidades_disponibles(enemigo)
    opciones = []
    pesos = []

    vida_enemigo = stats_enemigo.get("salud", 0)
    vida_max_enemigo = stats_enemigo.get("salud_max", 1)
    vida_jugador = stats_jugador.get("salud", 0)
    vida_max_jugador = stats_jugador.get("salud_max", 1)
    estados_jugador = stats_jugador.get("estados", [])

    for habilidad in habilidades:
        tipo = str(leer_efecto(habilidad, "tipo", "")).lower()
        if tipo not in ["daño", "curacion", "negativo", "buff", "debuff"]:
            continue

        peso = 1

        if tipo == "daño":
            escala = float(leer_efecto(habilidad, "escala_ataque", 1.0))
            bono = int(leer_efecto(habilidad, "valor", 0))
            danio_estimado = int(stats_enemigo["ataque"] * escala) + bono

            if vida_jugador <= danio_estimado:
                peso = 10
            elif vida_jugador < vida_max_jugador * 0.4:
                peso = 5
            else:
                peso = 3

        elif tipo == "curacion":
            escala = float(leer_efecto(habilidad, "escala_salud", 0.0))
            bono = int(leer_efecto(habilidad, "valor", 0))
            cura_estim = int(stats_enemigo["salud_max"] * escala) + bono

            if vida_enemigo <= vida_max_enemigo * 0.4:
                peso = 6
            elif vida_enemigo < vida_max_enemigo:
                peso = 3
            else:
                peso = 1

        elif tipo == "negativo":
            estado_objetivo = leer_efecto(habilidad, "estado")
            ya_aplicado = any(
                e["tipo"] == "negativo" and e.get("estado") == estado_objetivo
                for e in estados_jugador
            )
            peso = 4 if not ya_aplicado else 1

        elif tipo in ["buff", "debuff"]:
            stat = leer_efecto(habilidad, "stat")
            peso = evaluar_buff_o_debuff(tipo, stat, stats_enemigo, stats_jugador)

        opciones.append(habilidad)
        pesos.append(peso)

    opciones.append("basico")
    pesos.append(2)

    return choices(opciones, weights=pesos, k=1)[0]


# ============================
# EJECUCIÓN COMPLETA DEL TURNO ENEMIGO
# ============================

def ejecutar_accion_enemiga(enemigo, stats_enemigo, stats_jugador, log):
    nivel_jugador = stats_jugador.get("nivel", 1)
    eleccion = ia_enemiga(enemigo, stats_enemigo, stats_jugador)

    if eleccion == "basico":
        danio, mensaje = accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador)
    else:
        danio, mensaje = usar_habilidad_enemigo(eleccion, stats_enemigo, stats_jugador, enemigo, log)

    log.append(mensaje)
    return danio
