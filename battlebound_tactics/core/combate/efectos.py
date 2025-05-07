from jugador import tirada
def aplicar_estado(stats_temporales, estado_nuevo):
    """
    Aplica un nuevo estado a las estadísticas temporales.

    Si ya existe un estado del mismo tipo, lo sobrescribe.
    Si no existe, lo añade como un nuevo estado.

    Args:
        stats_temporales (dict): Estadísticas actuales del jugador en combate.
        estado_nuevo (dict): Estado que se quiere aplicar.
    """
    stats_temporales.setdefault("estados", [])
    tipo_nuevo = estado_nuevo["tipo"]

    for i, estado in enumerate(stats_temporales["estados"]):
        if estado["tipo"] == tipo_nuevo:
            stats_temporales["estados"][i] = estado_nuevo
            return

    stats_temporales["estados"].append(estado_nuevo)

def procesar_estados(stats_temporales, jugador):
    """
    Procesa todos los estados activos del jugador.

    - Aplica efectos negativos (por ejemplo, daño por veneno).
    - Aplica buffs acumulables.
    - Reduce la duración de todos los estados.

    Args:
        stats_temporales (dict): Estadísticas actuales del jugador.
        jugador (object): Instancia del jugador.

    Returns:
        list: Lista de mensajes con los efectos aplicados.
    """
    mensajes = []
    aplicar_buffs = []

    for estado in stats_temporales.get("estados", []):
        tipo = estado["tipo"]

        if tipo.startswith("negativo_"):
            if "veneno" in tipo:
                danio = estado["valor"]
                stats_temporales["salud"] = max(1, stats_temporales["salud"] - danio)
                mensajes.append(f"{jugador.nombre} sufre {danio} puntos de daño por veneno.")

        elif tipo.startswith("buff_"):
            aplicar_buffs.append(estado)

        estado["duracion"] -= 1

    for buff in aplicar_buffs:
        stat = buff["stat"]
        valor = buff["valor"]
        stats_temporales[stat] += valor
        mensajes.append(f"{jugador.nombre} tiene un aumento de {valor} en {stat} debido a un buff.")

    return mensajes

def limpiar_estados_expirados(stats_temporales):
    """
    Elimina todos los estados que tienen duración 0 o menor.
    """
    stats_temporales["estados"] = [
        estado for estado in stats_temporales.get("estados", [])
        if estado["duracion"] > 0
    ]

def remover_estado(stats_temporales, tipo):
    """
    Elimina un estado específico por tipo.
    """
    stats_temporales["estados"] = [
        estado for estado in stats_temporales.get("estados", [])
        if estado["tipo"] != tipo
    ]

def remover_estados_negativos(stats_temporales):
    """
    Elimina todos los estados negativos actuales.
    """
    stats_temporales["estados"] = [
        estado for estado in stats_temporales.get("estados", [])
        if not estado["tipo"].startswith("negativo_")
    ]

def aplicar_efecto_contrario(efecto, stats_objetivo, objetivo, log_combate):
    """
    Aplica un efecto negativo o buff con una probabilidad.

    Si la tirada es exitosa, se añade el estado. Si no, se informa que fue resistido.
    """
    prob = efecto.get("probabilidad", 1.0)
    if tirada(prob):
        estado = {
            "tipo": efecto["tipo"],
            "valor": efecto["valor"],
            "duracion": efecto["duracion"]
        }
        aplicar_estado(stats_objetivo, estado)
        log_combate.append(f"¡{objetivo.nombre} ha recibido el efecto {efecto['tipo']}!")
    else:
        log_combate.append(f"{objetivo.nombre} resistió el efecto {efecto['tipo']}.")