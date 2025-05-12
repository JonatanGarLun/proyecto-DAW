from globales.probabilidades import tirada

def aplicar_estado(stats_temporales, estado_nuevo):
    stats_temporales.setdefault("estados", [])
    if estado_nuevo.get("duracion", 0) <= 0:
        return

    tipo = estado_nuevo["tipo"]
    if tipo in ["buff", "debuff"] and estado_nuevo.get("porcentaje"):
        estado_nuevo["porcentaje"] = float(estado_nuevo["porcentaje"])

    for estado in stats_temporales["estados"]:
        if tipo == "negativo" and estado.get("estado") == estado_nuevo.get("estado"):
            estado["duracion"] = estado_nuevo["duracion"]
            estado["valor"] = max(estado["valor"], estado_nuevo["valor"])
            return
        elif tipo in ["buff", "debuff"] and estado.get("stat") == estado_nuevo.get("stat"):
            if estado.get("porcentaje") == estado_nuevo.get("porcentaje"):
                estado["duracion"] = estado_nuevo["duracion"]
                estado["valor"] = max(estado["valor"], estado_nuevo["valor"])
                return

    stats_temporales["estados"].append(estado_nuevo)


def procesar_estados(stats_temporales, jugador):
    mensajes = []
    aplicar_buffs, aplicar_debuffs = [], []

    for estado in stats_temporales.get("estados", []):
        tipo = estado["tipo"]
        if tipo == "negativo":
            danio = estado["valor"]
            stats_temporales["salud"] = max(1, stats_temporales["salud"] - danio)
            mensajes.append(f"{jugador.nombre} sufre {danio} puntos de daño por {estado['estado']}.")
        elif tipo == "buff":
            aplicar_buffs.append(estado)
        elif tipo == "debuff":
            aplicar_debuffs.append(estado)
        estado["duracion"] -= 1

    for buff in aplicar_buffs:
        incremento = int(stats_temporales[buff["stat"]] * buff["valor"]) if buff.get("porcentaje") else buff["valor"]
        stats_temporales[buff["stat"]] += incremento
        mensajes.append(f"{jugador.nombre} gana {incremento} extra en {buff['stat']} gracias a un buff.")

    for debuff in aplicar_debuffs:
        reduccion = int(stats_temporales[debuff["stat"]] * debuff["valor"]) if debuff.get("porcentaje") else debuff["valor"]
        stats_temporales[debuff["stat"]] = max(0, stats_temporales[debuff["stat"]] - reduccion)
        mensajes.append(f"{jugador.nombre} pierde {reduccion} en {debuff['stat']} debido a un debuff.")

    return mensajes


def limpiar_estados_expirados(stats_temporales):
    stats_temporales["estados"] = [e for e in stats_temporales.get("estados", []) if e["duracion"] > 0]


def remover_estado(stats_temporales, tipo, identificador=None):
    def coincide(e):
        if e["tipo"] != tipo:
            return False
        if tipo == "negativo":
            return e.get("estado") == identificador or identificador is None
        if tipo in ["buff", "debuff"]:
            return e.get("stat") == identificador or identificador is None
        return False

    stats_temporales["estados"] = [e for e in stats_temporales["estados"] if not coincide(e)]


def aplicar_efecto_contrario(efecto, stats_objetivo, objetivo, log_combate=None):
    if not tirada(efecto.get("probabilidad", 1.0)):
        nombre = efecto.get("estado") or efecto.get("stat") or "efecto desconocido"
        if log_combate:
            log_combate.append(f"{objetivo.nombre} resistió el efecto '{nombre}'.")
        return

    estado = {
        "tipo": efecto["tipo"],
        "valor": efecto["valor"],
        "duracion": efecto["duracion"]
    }
    if efecto["tipo"] == "negativo":
        estado["estado"] = efecto["estado"]
    elif efecto["tipo"] in ["buff", "debuff"]:
        estado["stat"] = efecto["stat"]
        estado["porcentaje"] = float(efecto.get("porcentaje", False))

    aplicar_estado(stats_objetivo, estado)

    if log_combate:
        tipo = efecto["tipo"]
        desc = f"{objetivo.nombre} ha recibido un {'estado negativo' if tipo == 'negativo' else tipo}."
        log_combate.append(desc)


def listar_estados_activos(stats_temporales):
    descripciones = []
    for estado in stats_temporales.get("estados", []):
        tipo, duracion = estado["tipo"], estado["duracion"]
        if tipo == "negativo":
            descripciones.append(f"Estado negativo: {estado['estado']} ({estado['valor']} daño/turno, {duracion} turnos)")
        elif tipo in ["buff", "debuff"]:
            valor = f"{int(estado['valor']*100)}%" if estado.get("porcentaje") else str(estado["valor"])
            simbolo = "+" if tipo == "buff" else "-"
            descripciones.append(f"{tipo.capitalize()}: {estado['stat']} ({simbolo}{valor}, {duracion} turnos)")
    return descripciones


def estado_activo(stats_temporales, tipo, identificador):
    for estado in stats_temporales.get("estados", []):
        if estado["tipo"] == tipo:
            if tipo == "negativo" and estado.get("estado") == identificador:
                return True
            if tipo in ["buff", "debuff"] and estado.get("stat") == identificador:
                return True
    return False
