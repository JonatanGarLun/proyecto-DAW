def leer_efecto(habilidad, campo, default=None):
    """
    Devuelve un campo del JSON 'efecto' o del modelo plantilla asociado.
    Soporta habilidades del jugador (efecto directo) y del enemigo.
    """
    if hasattr(habilidad, "efecto") and isinstance(habilidad.efecto, dict):
        return habilidad.efecto.get(campo, default)

    # Debido a un cambio en la lógica de las habilidades del enemigo este fragmento de código es inútil
    if hasattr(habilidad, "plantilla") and hasattr(habilidad.plantilla, "efecto"):
        return habilidad.plantilla.efecto.get(campo, default)

    return default


def leer_efectos(habilidad):
    """
    Devuelve una lista de efectos. Permite:
    - Habilidad con un solo efecto (dict)
    - Habilidad con múltiples efectos (efectos: [...])
    """
    efecto = leer_efecto(habilidad, "efecto", {})

    if isinstance(efecto, list):
        return efecto

    if isinstance(efecto, dict):
        return efecto.get("efectos", [efecto])

    return []
