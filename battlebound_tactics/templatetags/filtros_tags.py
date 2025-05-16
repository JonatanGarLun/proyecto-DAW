from django import template

register = template.Library()

@register.filter
def to(value, arg):
    """Uso: {% for i in 0|to:10 %} → itera de 0 a 9"""
    try:
        return range(int(value), int(arg))
    except:
        return []