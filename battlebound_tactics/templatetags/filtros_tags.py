import math

from django import template

register = template.Library()


@register.filter
def to(value, arg):
    """Uso: {% for i in 0|to:10 %} → itera de 0 a 9"""
    try:
        return range(int(value), int(arg))
    except:
        return []


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
