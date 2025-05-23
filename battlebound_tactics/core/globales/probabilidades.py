import random

def tirada(probabilidad):
    """
    Realiza una tirada aleatoria según una probabilidad (valor entre 0.0 y 1.0).
    """
    probabilidad = max(0.0, min(probabilidad, 1.0))
    return random.random() < probabilidad


def obtener_probabilidades_por_clase(clase):
    """
    Devuelve un diccionario con las probabilidades de crítico, esquivar y ataque adicional
    según la clase del jugador o enemigo.
    """
    clases = {
        "GUERRERO": {"critico": 0.15, "esquivar": 0.04, "adicional": 0.10},
        "ARQUERO": {"critico": 0.22, "esquivar": 0.18, "adicional": 0.22},
        "MAGO": {"critico": 0.17, "esquivar": 0.05, "adicional": 0.12},
        "LUCHADOR": {"critico": 0.16, "esquivar": 0.07, "adicional": 0.14},
        "ESPIRITUALISTA": {"critico": 0.18, "esquivar": 0.09, "adicional": 0.13},
        "ASTRAL": {"critico": 0.20, "esquivar": 0.10, "adicional": 0.18},
    }
    return clases.get(clase.upper(), {"critico": 0.10, "esquivar": 0.10, "adicional": 0.10})


def critico(objetivo):
    """
    Determina si se produce un golpe crítico en función de la clase del objetivo.
    """
    if hasattr(objetivo, "clase") and isinstance(objetivo.clase, str):
        prob = obtener_probabilidades_por_clase(objetivo.clase)["critico"]
    else:
        prob = 0.10
    return tirada(prob)


def esquivar(objetivo):
    """
    Determina si el objetivo esquiva un ataque.
    """
    if hasattr(objetivo, "clase") and isinstance(objetivo.clase, str):
        prob = obtener_probabilidades_por_clase(objetivo.clase)["esquivar"]
    else:
        prob = 0.10
    return tirada(prob)


def adicional(objetivo):
    """
    Determina si el objetivo realiza un ataque adicional.
    """
    if hasattr(objetivo, "clase") and isinstance(objetivo.clase, str):
        prob = obtener_probabilidades_por_clase(objetivo.clase)["adicional"]
    else:
        prob = 0.10
    return tirada(prob)