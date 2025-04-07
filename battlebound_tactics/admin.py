from django.contrib import admin
from .models import (
    Jugador, Mochila, Objeto, ObjetoEnMochila,
    Arma, Accesorio, Pasiva,
    HiddenPotential, HiddenPotentialNodeTemplate,
    Combate, Turno,
    Estado, EstadoActivo,
    Enemigo, Jefe
)

# -----------------------
# Registro de modelos
# -----------------------

admin.site.register(Jugador)
admin.site.register(Mochila)
admin.site.register(Objeto)
admin.site.register(ObjetoEnMochila)

admin.site.register(Arma)
admin.site.register(Accesorio)
admin.site.register(Pasiva)

admin.site.register(HiddenPotential)
admin.site.register(HiddenPotentialNodeTemplate)

admin.site.register(Combate)
admin.site.register(Turno)

admin.site.register(Estado)
admin.site.register(EstadoActivo)

admin.site.register(Enemigo)
admin.site.register(Jefe)
