def leer_efecto(habilidad, campo, default=None):
    """
    Devuelve un campo del JSON 'efecto' o del modelo plantilla asociado.
    Soporta habilidades del jugador (efecto directo) y del enemigo (plantilla).
    """
    if hasattr(habilidad, "efecto") and isinstance(habilidad.efecto, dict):
        return habilidad.efecto.get(campo, default)

    if hasattr(habilidad, "plantilla") and hasattr(habilidad.plantilla, "efecto"):
        return habilidad.plantilla.efecto.get(campo, default)

    return default


def leer_efectos(habilidad):
    """
    Devuelve una lista de efectos. Permite:
    - Habilidad con un solo efecto (dict)
    - Habilidad con múltiples efectos (efectos: [...])
    - Plantilla de enemigo
    """
    efecto = leer_efecto(habilidad, "efecto", {})

    if isinstance(efecto, list):
        return efecto

    if isinstance(efecto, dict):
        return efecto.get("efectos", [efecto])

    return []
