from random import choices
from battlebound_tactics.core.combate.utils_combate import leer_efecto
from battlebound_tactics.core.globales.probabilidades import critico, adicional
from battlebound_tactics.core.combate.efectos import aplicar_efecto_contrario, aplicar_estado
from battlebound_tactics.core.globales.probabilidades import esquivar
from battlebound_tactics.models import Combate, ActivaEnemigo


# ============================
# FUNCIONES AUXILIARES INTERNAS
# ============================

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
        mensaje = f"⚔️ ¡{enemigo.nombre} desata un golpe crítico con una fuerza castatrófica!"
    else:
        golpe = int(round(golpe))
        mensaje = f"{enemigo.nombre} lanza un ataque directo, sin florituras."

    return golpe, mensaje


def ataque_adicional_enemigo(stats_enemigo, enemigo, nivel_jugador):

    if adicional(enemigo):
        golpe, mensaje_base = accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador)
        mensaje = f"💥 {enemigo.nombre} detecta una abertura y ataca sin piedad con un golpe extra. {mensaje_base}"
        return golpe, mensaje
    else:
        mensaje = f"⚠️ {enemigo.nombre} trató de sorprender con un segundo golpe, ¡pero fue anticipado y bloqueado!"
        return 0, mensaje



def calcular_golpe_recibido_enemigo(golpe, enemigo, stats_temporales):
    """
    Calcula el daño recibido considerando defensa y posibilidad de esquivar.
    Aplica un daño mínimo del 1% de salud máxima.

    Args:
        golpe (int): Daño del ataque recibido.
        enemigo: Objeto Enemigo.
        stats_temporales (dict): Estadísticas actuales del jugador.

    Returns:
        tuple: Daño final recibido y mensaje descriptivo.
    """
    defensa = stats_temporales["defensa"]

    if esquivar(enemigo):
        mensaje = f"Gracias a la velocidad y a la estrategia de {enemigo.nombre}, ha logrado evitar el ataque."
        return 0, mensaje

    danio = golpe - defensa

    salud_max = stats_temporales["salud_max"]
    umbral_minimo = max(1, int(salud_max * 0.01))

    if danio <= umbral_minimo:
        danio = umbral_minimo
        mensaje = f"🛡️ {enemigo.nombre} detuvo casi todo el impacto, pero aún sufre {danio} de daño residual."

    else:
        mensaje = f"{enemigo.nombre} recibe el golpe del enemigo de lleno, ¡se ha llevado una buena!"

    return danio, mensaje


# ============================
# COOLDOWNS
# ============================

def reducir_cooldowns(combate: "Combate") -> None:
    """
    Reduce en 1 todos los cooldowns activos del enemigo en este combate.
    """
    cd = combate.cooldowns_enemigo or {}
    nuevos_cd = {nombre: max(0, val - 1) for nombre, val in cd.items()}
    combate.cooldowns_enemigo = nuevos_cd
    combate.save()


def cooldown_disponible(habilidad: "ActivaEnemigo", combate: "Combate") -> bool:
    """
    Verifica si la habilidad está disponible (cooldown en 0).
    """
    nombre = habilidad.nombre
    cooldowns = combate.cooldowns_enemigo or {}
    return cooldowns.get(nombre, 0) == 0


def aplicar_cooldown(habilidad: "ActivaEnemigo", combate: "Combate") -> None:
    """
    Aplica el cooldown de una habilidad enemiga en el estado del combate.
    """
    cooldown_valor = habilidad.efecto.get("cooldown", 1)
    nombre = habilidad.nombre
    cooldowns = combate.cooldowns_enemigo or {}
    cooldowns[nombre] = cooldown_valor
    combate.cooldowns_enemigo = cooldowns
    combate.save()


# ============================
# USO DE HABILIDADES
# ============================

def usar_habilidad_enemigo(habilidad, stats_enemigo, stats_jugador, enemigo, log, jugador):
    tipo = str(leer_efecto(habilidad, "tipo", "")).lower()
    cooldown = leer_efecto(habilidad, "cooldown", 1)

    resultado = 0
    mensaje = ""

    if tipo == "daño":
        escala = float(leer_efecto(habilidad, "escala_ataque", 1.0))
        bono = int(leer_efecto(habilidad, "valor", 0))
        resultado = int(stats_enemigo["ataque"] * escala) + bono
        mensaje = f"🔥 {enemigo.nombre} desata {habilidad.nombre} causando {resultado} de daño directo."

    elif tipo == "curacion":
        escala = float(leer_efecto(habilidad, "escala_salud", 0.0))
        bono = int(leer_efecto(habilidad, "valor", 0))
        resultado = int(stats_enemigo["salud_max"] * escala) + bono
        stats_enemigo["salud"] = min(stats_enemigo["salud_max"], stats_enemigo["salud"] + resultado)
        mensaje = f"✨ {enemigo.nombre} invoca {habilidad.nombre} y recupera {resultado} de vitalidad."

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
        aplicar_efecto_contrario(efecto, stats_jugador, objetivo=jugador, log_combate=log)
        mensaje = f"🌀 {enemigo.nombre} canaliza {habilidad.nombre} buscando cambiar el destino del combate."

    else:
        mensaje = f"❌ {enemigo.nombre} intenta activar su habilidad, pero algo falla... no sucede nada."
        resultado = None

    return resultado, mensaje


# ============================
# IA DEL ENEMIGO
# ============================

def ia_enemiga(stats_enemigo, stats_jugador, habilidades_disponibles):
    opciones = []
    pesos = []

    vida_enemigo = stats_enemigo.get("salud", 0)
    vida_max_enemigo = stats_enemigo.get("salud_max", 1)
    vida_jugador = stats_jugador.get("salud", 0)
    vida_max_jugador = stats_jugador.get("salud_max", 1)
    estados_jugador = stats_jugador.get("estados", [])

    for habilidad in habilidades_disponibles:
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

# def ejecutar_accion_enemiga(enemigo, stats_enemigo, stats_jugador, log, jugador):
#     nivel_jugador = stats_jugador.get("nivel", 1)
#     eleccion = ia_enemiga(enemigo, stats_enemigo, stats_jugador)
#
#     if eleccion == "basico":
#         danio, mensaje = accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador)
#     else:
#         danio, mensaje = usar_habilidad_enemigo(eleccion, stats_enemigo, stats_jugador, enemigo, log, jugador)
#
#     log.append(mensaje)
#     return danio


def ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log, combate):
    log.append(f"TURNO {enemigo.nombre}")

    # Reducir cooldowns al inicio del turno
    reducir_cooldowns(combate)

    # Obtener habilidades disponibles
    habilidades = [enemigo.habilidad_1, enemigo.habilidad_2, enemigo.habilidad_3]
    habilidades_disponibles = [h for h in habilidades if h and cooldown_disponible(h, combate)]

    # Elegir acción: habilidad o ataque básico
    eleccion = ia_enemiga(stats_enemigo, stats_jugador, habilidades_disponibles)

    if eleccion == "basico" or not habilidades_disponibles:
        # Ataque básico
        danio, mensaje = accion_basica_enemigo(stats_enemigo, enemigo, jugador.nivel)
        stats_jugador["salud"] = max(0, stats_jugador["salud"] - danio)
        log.append(mensaje)

        # Ataque adicional
        danio, mensaje = ataque_adicional_enemigo(stats_enemigo, enemigo, jugador.nivel)
        stats_jugador["salud"] = max(0, stats_jugador["salud"] - danio)
        log.append(mensaje)

    else:
        # Usar habilidad
        resultados, mensaje = usar_habilidad_enemigo(eleccion, stats_enemigo, stats_jugador, enemigo,jugador, log)
        aplicar_cooldown(eleccion, combate)

        if not resultados:
            resultados = []

        if isinstance(resultados, int):
            resultados = [("daño", resultados)]

        for tipo, dato in resultados:
            if tipo == "daño":
                stats_jugador["salud"] = max(0, stats_jugador["salud"] - dato)
            elif tipo == "curacion":
                stats_enemigo["salud"] = min(stats_enemigo["salud_max"], stats_enemigo["salud"] + dato)
            elif tipo in ["buff", "debuff", "negativo"]:
                objetivo = stats_enemigo if tipo == "buff" else stats_jugador
                aplicar_estado(objetivo, dato)

        if mensaje:
            log.append(mensaje)

    if stats_jugador["salud"] <= 0:
        from combate.utils_resolvedor import resolver_derrota
        return resolver_derrota(request, jugador, combate)

    return None
