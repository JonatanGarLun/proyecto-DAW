from django import template

from battlebound_tactics.models import Jugador

register = template.Library()

@register.filter
def tiene_jugador(user):
    try:
        return user.is_authenticated and user.jugador is not None
    except Jugador.DoesNotExist:
        return False