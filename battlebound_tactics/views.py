from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import RegistroForm
from .models import Jugador, Combate, Enemigo
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from battlebound_tactics.core.globales.estadisticas import obtener_stats_temporales
from battlebound_tactics.core.combate.efectos import (
    aplicar_estado,
    procesar_estados,
    limpiar_estados_expirados
)
from battlebound_tactics.core.combate.jugador import (
    accion_basica,
    uso_habilidad,
    actualizar_stats_finales
)
from battlebound_tactics.core.combate.enemigos import (
    ia_enemiga,
    usar_habilidad_enemigo,
    accion_basica_enemigo
)


class InicioPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener la instancia de Jugador vinculada al usuario
        jugador = get_object_or_404(Jugador, user=self.request.user)

        # Opciones del carrusel
        # Podemos agregar/editar más opciones; cada opción tiene:
        # - nombre: texto que se muestra
        # - imagen: ruta de la imagen del menú (imagen pequeña que aparece abajo)
        # - url: hacia dónde navega cuando se selecciona la opción
        # - imagen_central: la imagen que se mostrará en el centro al seleccionar esta opción (imagen grande que ocupa toda la pantalla)
        opciones = [
            {
                'nombre': 'Combate',
                'imagen': '/static/resources/menus/combate.png', #Imagen pequeña
                'url': '/combate/',
                'imagen_central': '/static/resources/menus/combate.png', #Imagen grande
            },
            {
                'nombre': 'Mapa',
                'imagen': '/static/resources/menus/mapas.png',  # Imagen pequeña
                'url': '/mapa/',
                'imagen_central': '/static/resources/menus/mapas.png',  # Imagen grande
            },
            {
                'nombre': 'Inventario',
                'imagen': '/static/resources/menus/inventario.png',  # Imagen pequeña
                'url': '/inventario/',
                'imagen_central': '/static/resources/menus/inventario.png',  # Imagen grande
            },
            {
                'nombre': 'Tienda',
                'imagen': '/static/resources/menus/tienda.png',  # Imagen pequeña
                'url': '/tienda/',
                'imagen_central': '/static/resources/menus/tienda.png',  # Imagen grande
            },
            {
                'nombre': 'Posada',
                'imagen': '/static/resources/menus/posada.png',  # Imagen pequeña
                'url': '/posada/',
                'imagen_central': '/static/resources/menus/posada.png',  # Imagen grande
            },
            {
                'nombre': 'Estadísticas',
                'imagen': '/static/resources/menus/estadisticas.png', #Imagen pequeña
                'url': '/estadísticas/',
                'imagen_central': '/static/resources/menus/estadisticas.png', #Imagen grande
            },
        ]

        context['jugador'] = jugador
        context['porcentaje_salud'] = int((jugador.salud / jugador.salud_maxima) * 100)
        context['porcentaje_energia'] = int((jugador.energia_espiritual / jugador.energia_espiritual_maxima) * 100)
        context['porcentaje_exp'] = int((jugador.experiencia / jugador.experiencia_maxima) * 100)
        context['opciones'] = opciones

        return context

class MapaContinentePageView(LoginRequiredMixin, TemplateView):
    template_name ='app/mapa_continente.html'

class RegionPageView(LoginRequiredMixin, TemplateView):
    template_name ='app/mapa_region.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugador'] = get_object_or_404(Jugador, user=self.request.user)
        context['enemigos'] = Enemigo.objects.all()
        context['prueba'] = Enemigo.objects.first()
        return context

class RegistroPageView(FormView):
    template_name = 'app/registro_usuario.html'
    form_class = RegistroForm
    success_url = reverse_lazy('inicio')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginUserView(LoginView):
    template_name = 'registration/login.html'

class EstadisticasPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/registro_usuario.html'


# El comabte esta hecho de tal forma que nosotros cogemos las stats del enemigo y creamos un "enemigo nuevo" temporal que es con quien pelaremos,
# gracias a esto no tenemos que modificar al enemigo en la base de datos ya que no lo "usamos" realmente
@login_required
def combate(request, combate_id):
    # === 1. CARGA DE COMBATE Y PARTICIPANTES ===

    combate_creado = get_object_or_404(Combate, id=combate_id)
    jugador = combate_creado.jugador
    enemigo = combate_creado.enemigo
    log = []

    # ======== SEGURIDAD Y CONTROL DE ACCESO =========

    # Si el combate ya terminó, redirige a la pantalla de resultado
    if combate.finalizado:
        return redirect("resultado_combate", combate_id=combate.id)

    # === 2. CONTROLAMOS SI YA SE INICIÓ ESTE COMBATE EN LA SESIÓN ===
    combate_key = f"combate_{combate_creado.id}_iniciado"

    if not request.session.get(combate_key, False):
        # Primera vez: inicializamos stats
        stats_jugador = obtener_stats_temporales(jugador)
        stats_jugador["objeto"] = jugador
        stats_enemigo = obtener_stats_temporales(enemigo)
        stats_enemigo["objeto"] = enemigo

        request.session["stats_jugador"] = stats_jugador
        request.session["stats_enemigo"] = stats_enemigo
        request.session[combate_key] = True
    else:
        # Ya está iniciado: recuperamos
        stats_jugador = request.session["stats_jugador"]
        stats_enemigo = request.session["stats_enemigo"]

    # === 3. PROCESAR EFECTOS DE ESTADO (INICIO DE TURNO) ===
    log += procesar_estados(stats_jugador, jugador)
    log += procesar_estados(stats_enemigo, enemigo)

    limpiar_estados_expirados(stats_jugador)
    limpiar_estados_expirados(stats_enemigo)

    # === 4. VERIFICAR DERROTAS POR EFECTOS ===
    if stats_jugador["salud"] <= 0:
        log.append(f"💀 {jugador.nombre} ha sucumbido a los efectos del combate_creado...")
        actualizar_stats_finales(jugador, stats_jugador)
        combate_creado.finalizado = True
        combate_creado.resultado = "derrota"
        combate_creado.save()

        request.session.pop("stats_jugador", None)
        request.session.pop("stats_enemigo", None)
        request.session.pop(combate_key, None)

        return render(request, "app/resultado.html", {
            "log": log,
            "ganador": enemigo,
            "combate_creado": combate_creado,
        })

    if stats_enemigo["salud"] <= 0:
        log.append(f"🎉 ¡{enemigo.nombre} no pudo resistir los efectos negativos y ha caído!")
        actualizar_stats_finales(jugador, stats_jugador)
        combate_creado.finalizado = True
        combate_creado.resultado = "victoria"
        combate_creado.save()

        request.session.pop("stats_jugador", None)
        request.session.pop("stats_enemigo", None)
        request.session.pop(combate_key, None)

        return render(request, "app/resultado.html", {
            "log": log,
            "ganador": jugador,
            "combate_creado": combate_creado,
        })

    # === 5. ACCIÓN DEL JUGADOR ===
    if request.method == "POST":
        accion = request.POST.get("accion")

        if accion == "atacar":
            danio, mensaje = accion_basica(stats_jugador, jugador)
            stats_enemigo["salud"] = max(1, stats_enemigo["salud"] - danio)
            log.append(mensaje)

        elif accion in ["habilidad_1", "habilidad_2", "habilidad_3"]:
            resultados, mensaje = uso_habilidad(jugador, accion, stats_jugador)
            log.append(mensaje)

            for resultado in resultados:
                tipo = resultado[0]
                if tipo == "daño":
                    danio = resultado[1]
                    stats_enemigo["salud"] = max(1, stats_enemigo["salud"] - danio)

                elif tipo == "curacion":
                    curacion = resultado[1]
                    stats_jugador["salud"] = min(stats_jugador["salud_max"], stats_jugador["salud"] + curacion)

                elif tipo == "buff":
                    stat, valor, duracion = resultado[1:]
                    estado = {"tipo": "buff", "stat": stat, "valor": valor, "duracion": duracion}
                    aplicar_estado(stats_jugador, estado)

                elif tipo == "debuff":
                    stat, valor, duracion = resultado[1:]
                    estado = {"tipo": "debuff", "stat": stat, "valor": valor, "duracion": duracion}
                    aplicar_estado(stats_enemigo, estado)

                elif tipo == "negativo":
                    estado_nombre, valor, duracion = resultado[1:]
                    estado = {"tipo": "negativo", "estado": estado_nombre, "valor": valor, "duracion": duracion}
                    aplicar_estado(stats_enemigo, estado)

        else:
            log.append("⚠️ No permitimos ese tipo de acción en estas tierras. Cuidado con lo que haces...")

        # === 6. VERIFICAR DERROTA DEL ENEMIGO TRAS ATAQUE ===
        if stats_enemigo["salud"] <= 0:
            log.append(f"🎉 ¡Has derrotado a {enemigo.nombre}!")
            actualizar_stats_finales(jugador, stats_jugador)
            combate_creado.finalizado = True
            combate_creado.resultado = "victoria"
            combate_creado.save()

            request.session.pop("stats_jugador", None)
            request.session.pop("stats_enemigo", None)
            request.session.pop(combate_key, None)

            return render(request, "app/resultado.html", {
                "log": log,
                "ganador": jugador,
                "combate_creado": combate_creado,
            })

        # === 7. TURNO DEL ENEMIGO ===
        eleccion = ia_enemiga(enemigo, stats_enemigo, stats_jugador)
        if eleccion == "basico":
            danio, mensaje = accion_basica_enemigo(stats_enemigo, enemigo, jugador.nivel)
            stats_jugador["salud"] = max(1, stats_jugador["salud"] - danio)
            log.append(mensaje)
        else:
            resultado, mensaje = usar_habilidad_enemigo(eleccion, stats_enemigo, stats_jugador, enemigo, log)
            if isinstance(resultado, int):
                stats_jugador["salud"] = max(1, stats_jugador["salud"] - resultado)
            log.append(mensaje)

        # === 8. VERIFICAR DERROTA DEL JUGADOR ===
        if stats_jugador["salud"] <= 0:
            log.append(f"💀 {jugador.nombre} ha sido derrotado...")
            actualizar_stats_finales(jugador, stats_jugador)
            combate_creado.finalizado = True
            combate_creado.resultado = "derrota"
            combate_creado.save()

            request.session.pop("stats_jugador", None)
            request.session.pop("stats_enemigo", None)
            request.session.pop(combate_key, None)

            return render(request, "app/resultado.html", {
                "log": log,
                "ganador": enemigo,
                "combate_creado": combate_creado,
            })

    # === 9. GUARDAR STATS EN SESIÓN Y RENDER ===
    request.session["stats_jugador"] = stats_jugador
    request.session["stats_enemigo"] = stats_enemigo

    return render(request, "app/combate.html", {
        "combate_creado": combate_creado,
        "jugador": jugador,
        "enemigo": enemigo,
        "stats_jugador": stats_jugador,
        "stats_enemigo": stats_enemigo,
        "log": log,
    })

