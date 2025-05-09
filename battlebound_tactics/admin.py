from django.contrib import admin
from .models import (
    Jugador, Mochila, Objeto, ObjetoEnMochila,
    Arma, Accesorio, Pasiva,
    Combate,
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

admin.site.register(Combate)

admin.site.register(Enemigo)
admin.site.register(Jefe)
