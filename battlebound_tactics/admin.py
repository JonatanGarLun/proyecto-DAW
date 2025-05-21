from django.contrib import admin
from .models import (
    Jugador,
    Arma, Accesorio, Pasiva,
    Combate,
    Enemigo, Jefe, Activa
)

# -----------------------
# Registro de modelos
# -----------------------

admin.site.register(Jugador)
admin.site.register(Arma)
admin.site.register(Accesorio)
admin.site.register(Pasiva)
admin.site.register(Activa)
admin.site.register(Combate)
admin.site.register(Enemigo)
admin.site.register(Jefe)
