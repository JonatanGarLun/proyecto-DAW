from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from battlebound_tactics.models import Combate


class AccessUserMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        # Asegurarse de que el usuario esté autenticado
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Cargar el combate y comprobar acceso
        combate_id = kwargs.get("pk") or kwargs.get("combate_id")
        combate = get_object_or_404(Combate, id=combate_id)
        jugador = combate.jugador

        if request.user != jugador.user and not request.user.is_staff:
            # Usuario no autorizado
            return render(request, "errores/403_forbidden.html", status=403)

        # Usuario autorizado
        return super().dispatch(request, *args, **kwargs)  # type: ignore[attr-defined]
        # Como a Pycharm "no le gusta" el dispatch, he tenido que silenciar el "error", pero el código funciona correctamente
