from rest_framework import viewsets, filters
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.serializers import JugadorSerializer
from battlebound_tactics.models import Jugador


class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'nombre', 'victorias', 'derrotas', 'oro','nivel']
    ordering = ['victorias']
    pagination_class = CursorPagination

    def list(self, request, *args, **kwargs):
        jugadores = self.get_queryset()

        page = self.paginate_queryset(jugadores)
        data = []

        if page is not None:
            for jugador in page:
                total = jugador.victorias + jugador.derrotas
                porcentaje_victorias = f"{jugador.victorias / total * 100:.2f}%" if total > 0 else "N/A"

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
                        "habilidad_pasiva": jugador.habilidad_pasiva.efecto if jugador.habilidad_pasiva else "No tiene una pasiva asignada",
                        "habilidad_1": jugador.habilidad_1 if jugador.habilidad_1 else "Ninguna",
                        "habilidad_2": jugador.habilidad_2 if jugador.habilidad_2 else "Ninguna",
                        "habilidad_3": jugador.habilidad_3 if jugador.habilidad_3 else "Ninguna",
                    },
                    "victorias": jugador.victorias,
                    "derrotas": jugador.derrotas,
                    "porcentaje_victorias": porcentaje_victorias,
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
                    "arma": jugador.arma if jugador.arma else "Desarmado",
                    "accesorios": jugador.accesorio if jugador.accesorio else "Sin equipo"
                },
                "habilidades": {
                    "habilidad_pasiva": jugador.habilidad_pasiva.efecto if jugador.habilidad_pasiva else "No tiene una pasiva asignada",
                    "habilidad_1": jugador.habilidad_1 if jugador.habilidad_1 else "Ninguna",
                    "habilidad_2": jugador.habilidad_2 if jugador.habilidad_2 else "Ninguna",
                    "habilidad_3": jugador.habilidad_3 if jugador.habilidad_3 else "Ninguna",
                },
                "victorias": jugador.victorias,
                "derrotas": jugador.derrotas,
                "porcentaje_victorias": (
                    f"{jugador.victorias / (jugador.victorias + jugador.derrotas) * 100:.2f}%" if (jugador.victorias + jugador.derrotas) > 0 else "N/A"
                ), })
        return Response(data)


class ApiRootViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        return Response({
            'jugadores': request.build_absolute_uri(reverse('api:jugador-list', request=request)),
        })
