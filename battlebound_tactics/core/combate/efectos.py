from ..globales.probabilidades import tirada
from copy import deepcopy


def aplicar_estado(stats_temporales, estado_nuevo):
    stats_temporales.setdefault("estados", [])

    if estado_nuevo.get("duracion", 0) <= 0:
        return

    estado_copia = deepcopy(estado_nuevo)
    tipo = estado_copia["tipo"]

    # Verificamos si ya existe un estado del mismo tipo y objetivo
    for estado in stats_temporales["estados"]:
        mismo_estado = ((
            tipo == "negativo" and estado.get("estado") == estado_copia.get("estado")) or ( tipo in ["buff", "debuff"] and estado.get("stat") == estado_copia.get("stat")))
        if mismo_estado:
            # Si ya estaba aplicado y el nuevo es mejor, lo actualizamos
            if estado.get("valor", 0) < estado_copia.get("valor", 0):
                estado["valor"] = estado_copia["valor"]
                estado["duracion"] = estado_copia["duracion"]
            else:
                # Solo renovamos duración si no es mejor
                estado["duracion"] = max(estado["duracion"], estado_copia["duracion"])
            return  # No se vuelve a aplicar

    # Aplicar por primera vez
    if tipo in ["buff", "debuff"]:
        stat = estado_copia["stat"]
        valor = estado_copia["valor"]
        incremento = int(stats_temporales[stat] * valor) if estado_copia.get("porcentaje") else valor

        if tipo == "buff":
            stats_temporales[stat] += incremento
        else:
            stats_temporales[stat] = max(0, stats_temporales[stat] - incremento)

        estado_copia["aplicado"] = incremento
        estado_copia["activado"] = True
    else:
        estado_copia["activado"] = False  # se aplica en `procesar_estados`

    stats_temporales["estados"].append(estado_copia)


def procesar_estados(stats_temporales, objeto):
    """
    Aplica efectos de estado (veneno, buff, debuff, etc.) y reduce su duración.
    """
    mensajes = []
    nuevos_estados = []

    for estado in stats_temporales.get("estados", []):
        tipo = estado.get("tipo")
        duracion = estado.get("duracion", 0)
        if duracion <= 0:
            continue

        if tipo == "negativo":
            valor = estado.get("valor", 0)
            stats_temporales["salud"] = max(0, stats_temporales["salud"] - valor)
            mensajes.append(f"{objeto.nombre} sufre {valor} de daño por {estado.get('estado', 'efecto negativo')}.")

        elif tipo == "buff":
            if not estado.get("activado"):
                stat = estado["stat"]
                valor = estado["valor"]
                incremento = int(stats_temporales[stat] * valor) if estado.get("porcentaje") else valor
                stats_temporales[stat] += incremento
                estado["activado"] = True
                estado["aplicado"] = incremento
                mensajes.append(f"{objeto.nombre} gana {incremento} en {stat} por un buff.")

        elif tipo == "debuff":
            if not estado.get("activado"):
                stat = estado["stat"]
                valor = estado["valor"]
                reduccion = int(stats_temporales[stat] * valor) if estado.get("porcentaje") else valor
                stats_temporales[stat] = max(0, stats_temporales[stat] - reduccion)
                estado["activado"] = True
                estado["aplicado"] = reduccion
                mensajes.append(f"{objeto.nombre} pierde {reduccion} en {stat} por un debuff.")

        estado["duracion"] -= 1
        nuevos_estados.append(estado)

    stats_temporales["estados"] = nuevos_estados
    return mensajes


def limpiar_estados_expirados(stats_temporales):
    nuevos_estados = []

    for estado in stats_temporales.get("estados", []):
        if estado["duracion"] <= 0:
            if estado["tipo"] in ["buff", "debuff"] and estado.get("activado") and "aplicado" in estado:
                stat = estado.get("stat")
                valor = estado["aplicado"]
                if estado["tipo"] == "buff":
                    stats_temporales[stat] = max(0, stats_temporales[stat] - valor)
                else:
                    stats_temporales[stat] += valor
        else:
            nuevos_estados.append(estado)

    stats_temporales["estados"] = nuevos_estados


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
            descripciones.append(
                f"Estado negativo: {estado['estado']} ({estado['valor']} daño/turno, {duracion} turnos)")
        elif tipo in ["buff", "debuff"]:
            valor = f"{int(estado['valor'] * 100)}%" if estado.get("porcentaje") else str(estado["valor"])
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
