import math

from django import template

register = template.Library()

@register.filter
def porcentaje(valor, maximo):
    try:
        return math.ceil((valor / maximo) * 100)
    except (ZeroDivisionError, TypeError):
        return 0


@register.filter
def get_habilidad(jugador, index_str):
    index = int(index_str)
    return getattr(jugador, f"habilidad_{index}", None)

@register.filter
def decimal_a_porcentaje(valor):
    try:
        return valor * 100
    except TypeError:
        return valor

@register.filter
def obtener_habilidad(jugador, numero):
    return {
        "1": jugador.habilidad_1,
        "2": jugador.habilidad_2,
        "3": jugador.habilidad_3,
    }