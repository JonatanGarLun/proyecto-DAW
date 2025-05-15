def limpiar_sesion_combate(request, combate_id):
    request.session.pop("stats_jugador", None)
    request.session.pop("stats_enemigo", None)
    request.session.pop(f"combate_{combate_id}_iniciado", None)