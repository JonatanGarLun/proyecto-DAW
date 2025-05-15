from rest_framework import viewsets, filters
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import JugadorSerializer
from battlebound_tactics.models import Jugador


class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'nombre', 'victorias', 'derrotas']
    ordering = ['id']
    pagination_class = [CursorPagination]

    def list(self, request, *args, **kwargs):
        jugadores = self.get_queryset()

        page = self.paginate_queryset(jugadores)
        data = []

        if page is not None:
            for jugador in page:
                data.append({
                    "id_jugador": jugador.id,
                    "usuario": jugador.user.username,
                    "nombre_personaje": jugador.nombre,
                    "alineacion": jugador.alineacion,
                    "oro": jugador.oro,
                    "estadisticas": {
                        "clase": jugador.clase,
                        "nivel": jugador.nivel,
                        "experiencia_actual": jugador.experiencia,
                        "salud": jugador.salud_maxima,
                        "energia": jugador.energia_espiritual_maxima,
                        "ataque": jugador.ataque,
                        "defensa": jugador.defensa,
                        "velocidad": jugador.velocidad,
                    },
                    "equipo": {
                        "arma": jugador.arma if jugador.arma else "Ninguna",
                        "accesorios": jugador.accesorio if jugador.accesorio else "Ninguno"
                    },
                    "habilidades": {
                        "habilidad_pasiva": jugador.habilidad_pasiva,
                        "habilidad_1": jugador.habilidad_1 if jugador.habilidad_1 else "Ninguna",
                        "habilidad_2": jugador.habilidad_2 if jugador.habilidad_2 else "Ninguna",
                        "habilidad_3": jugador.habilidad_3 if jugador.habilidad_3 else "Ninguna",
                    },
                    "victorias": jugador.victorias,
                    "derrotas": jugador.derrotas,
                    "porcentaje_victorias": f"{jugador.victorias / (jugador.victorias + jugador.derrotas) * 100:.2f}%",
                })
            return self.get_paginated_response(data)

        for jugador in jugadores:
            data.append({
                "id_jugador": jugador.id,
                "usuario": jugador.user.username,
                "nombre_personaje": jugador.nombre,
                "alineacion": jugador.alineacion,
                "oro": jugador.oro,
                "estadisticas": {
                    "clase": jugador.clase,
                    "nivel": jugador.nivel,
                    "experiencia_actual": jugador.experiencia,
                    "salud": jugador.salud_maxima,
                    "energia": jugador.energia_espiritual_maxima,
                    "ataque": jugador.ataque,
                    "defensa": jugador.defensa,
                    "velocidad": jugador.velocidad,
                },
                "equipo": {
                    "arma": jugador.arma if jugador.arma else "Ninguna",
                    "accesorios": jugador.accesorio if jugador.accesorio else "Ninguno"
                },
                "habilidades": {
                    "habilidad_pasiva": jugador.habilidad_pasiva,
                    "habilidad_1": jugador.habilidad_1 if jugador.habilidad_1 else "Ninguna",
                    "habilidad_2": jugador.habilidad_2 if jugador.habilidad_2 else "Ninguna",
                    "habilidad_3": jugador.habilidad_3 if jugador.habilidad_3 else "Ninguna",
                },
                "victorias": jugador.victorias,
                "derrotas": jugador.derrotas,
                "porcentaje_victorias": f"{jugador.victorias / (jugador.victorias + jugador.derrotas) * 100:.2f}%",
            })
        return Response(data)
