from jugador import tirada

def aplicar_estado(stats_temporales, estado_nuevo):
    """
    Aplica un nuevo estado al jugador:
    - Solo puede existir un estado con el mismo tipo + identificador (stat/estado + porcentaje si aplica).
    - Si se intenta aplicar uno ya existente:
        - Reemplaza la duración.
        - Si el nuevo valor es mayor, se actualiza.
    - Si no existe, se añade.
    - Los estados con duración <= 0 se ignoran.
    """
    stats_temporales.setdefault("estados", [])

    if estado_nuevo.get("duracion", 0) <= 0:
        return  # Estado inválido.

    tipo = estado_nuevo["tipo"]
    if tipo in ["buff", "debuff"] and estado_nuevo.get("porcentaje"):
        estado_nuevo["porcentaje"] = float(estado_nuevo["porcentaje"])

    reemplazado = False

    for i, estado in enumerate(stats_temporales["estados"]):
        if tipo == "negativo":
            # Coincide tipo + estado
            if estado["tipo"] == "negativo" and estado["estado"] == estado_nuevo["estado"]:
                # Reemplazamos duración y valor si el nuevo es mayor
                estado["duracion"] = estado_nuevo["duracion"]
                if estado_nuevo["valor"] > estado["valor"]:
                    estado["valor"] = estado_nuevo["valor"]
                reemplazado = True
                break

        elif tipo in ["buff", "debuff"]:
            # Coincide tipo + stat + porcentaje
            if (
                estado["tipo"] == tipo and
                estado["stat"] == estado_nuevo["stat"] and
                estado.get("porcentaje", False) == estado_nuevo.get("porcentaje", False)
            ):
                estado["duracion"] = estado_nuevo["duracion"]
                if estado_nuevo["valor"] > estado["valor"]:
                    estado["valor"] = estado_nuevo["valor"]
                reemplazado = True
                break

    if not reemplazado:
        stats_temporales["estados"].append(estado_nuevo)


def procesar_estados(stats_temporales, jugador):
    """
    Procesa todos los estados activos:
    - Aplica daño por negativos.
    - Aplica buffs (aumentos) y debuffs (reducciones) a stats.
    - Reduce la duración de cada estado en 1.
    """
    mensajes = []
    aplicar_buffs = []
    aplicar_debuffs = []

    for estado in stats_temporales.get("estados", []):
        tipo = estado["tipo"]

        # --- NEGATIVOS ---
        if tipo == "negativo":
            efecto = estado["estado"]
            danio = estado["valor"]
            stats_temporales["salud"] = max(1, stats_temporales["salud"] - danio)
            mensajes.append(f"{jugador.nombre} sufre {danio} puntos de daño por {efecto}.")

        # --- BUFFS Y DEBUFFS ---
        elif tipo == "buff":
            aplicar_buffs.append(estado)

        elif tipo == "debuff":
            aplicar_debuffs.append(estado)

        estado["duracion"] -= 1  # Reducir duración

    # --- APLICAR BUFFS ---
    for buff in aplicar_buffs:
        stat = buff["stat"]
        valor = buff["valor"]
        porcentaje = buff.get("porcentaje", False)

        if porcentaje:
            incremento = int(stats_temporales[stat] * valor)
        else:
            incremento = valor

        stats_temporales[stat] += incremento
        mensajes.append(
            f"{jugador.nombre} gana {incremento} extra en {stat} gracias a un buff."
        )

    # --- APLICAR DEBUFFS ---
    for debuff in aplicar_debuffs:
        stat = debuff["stat"]
        valor = debuff["valor"]
        porcentaje = debuff.get("porcentaje", False)

        if porcentaje:
            reduccion = int(stats_temporales[stat] * valor)
        else:
            reduccion = valor

        stats_temporales[stat] -= reduccion
        stats_temporales[stat] = max(0, stats_temporales[stat])

        mensajes.append(
            f"{jugador.nombre} pierde {reduccion} en {stat} debido a un debuff."
        )

    return mensajes


def limpiar_estados_expirados(stats_temporales):
    """
    Elimina todos los estados cuya duración haya llegado a 0 o menos.
    """
    stats_temporales["estados"] = [
        estado for estado in stats_temporales.get("estados", [])
        if estado["duracion"] > 0
    ]


def remover_estado(stats_temporales, tipo, identificador=None):
    """
    Elimina un estado específico.
    - Para negativos: identificador = estado.
    - Para buffs/debuffs: identificador = stat.
    - Si identificador es None, borra todos los de ese tipo.
    """
    def coincide(estado):
        if estado["tipo"] != tipo:
            return False
        if tipo == "negativo" and identificador:
            return estado["estado"] == identificador
        if tipo in ["buff", "debuff"] and identificador:
            return estado["stat"] == identificador
        return identificador is None

    stats_temporales["estados"] = [
        estado for estado in stats_temporales.get("estados", [])
        if not coincide(estado)
    ]


def remover_estados_negativos(stats_temporales):
    """
    Elimina todos los estados negativos activos.
    """
    stats_temporales["estados"] = [
        estado for estado in stats_temporales.get("estados", [])
        if estado["tipo"] != "negativo"
    ]


def aplicar_efecto_contrario(efecto, stats_objetivo, objetivo, log_combate):
    """
    Aplica un estado (negativo, buff o debuff) con una probabilidad.
    - Si la tirada tiene éxito, se aplica.
    - Si falla, se informa en el log.
    """
    prob = efecto.get("probabilidad", 1.0)

    if tirada(prob):
        estado = {
            "tipo": efecto["tipo"],
            "valor": efecto["valor"],
            "duracion": efecto["duracion"]
        }

        if efecto["tipo"] == "negativo":
            estado["estado"] = efecto["estado"]

        elif efecto["tipo"] in ["buff", "debuff"]:
            estado["stat"] = efecto["stat"]
            porcentaje = efecto.get("porcentaje", False)
            estado["porcentaje"] = float(porcentaje) if porcentaje else False  # MEJORA


        aplicar_estado(stats_objetivo, estado)

        if efecto["tipo"] == "negativo":
            log_combate.append(
                f"¡{objetivo.nombre} ha recibido el estado negativo '{efecto['estado']}'!"
            )
        elif efecto["tipo"] == "buff":
            log_combate.append(
                f"{objetivo.nombre} ha recibido un buff en {efecto['stat']}."
            )
        elif efecto["tipo"] == "debuff":
            log_combate.append(
                f"{objetivo.nombre} ha recibido un debuff en {efecto['stat']}."
            )

    else:
        nombre = efecto.get("estado") or efecto.get("stat") or "efecto desconocido"
        log_combate.append(
            f"{objetivo.nombre} resistió el efecto '{nombre}'."
        )

def listar_estados_activos(stats_temporales):
    """
    Devuelve una lista de cadenas con una descripción legible de todos los estados activos.
    """
    descripciones = []

    for estado in stats_temporales.get("estados", []):
        tipo = estado["tipo"]
        duracion = estado["duracion"]

        if tipo == "negativo":
            descripciones.append(
                f"Estado negativo: {estado['estado']} ({estado['valor']} daño por turno, {duracion} turnos restantes)"
            )

        elif tipo == "buff":
            porcentaje = estado.get("porcentaje", False)
            if porcentaje:
                descripciones.append(
                    f"Buff: {estado['stat']} (+{int(estado['valor']*100)}%, {duracion} turnos restantes)"
                )
            else:
                descripciones.append(
                    f"Buff: {estado['stat']} (+{estado['valor']}, {duracion} turnos restantes)"
                )

        elif tipo == "debuff":
            porcentaje = estado.get("porcentaje", False)
            if porcentaje:
                descripciones.append(
                    f"Debuff: {estado['stat']} (-{int(estado['valor']*100)}%, {duracion} turnos restantes)"
                )
            else:
                descripciones.append(
                    f"Debuff: {estado['stat']} (-{estado['valor']}, {duracion} turnos restantes)"
                )

    return descripciones

def estado_activo(stats_temporales, tipo, identificador):
    """
    Comprueba si hay un estado activo de un tipo e identificador dado.
    - Para negativos: identificador = nombre del estado.
    - Para buffs/debuffs: identificador = stat.
    Devuelve True si existe, False si no.
    """
    for estado in stats_temporales.get("estados", []):
        if estado["tipo"] != tipo:
            continue
        if tipo == "negativo" and estado["estado"] == identificador:
            return True
        if tipo in ["buff", "debuff"] and estado["stat"] == identificador:
            return True
    return False