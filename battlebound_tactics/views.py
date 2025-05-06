import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import RegistroForm
from .models import Jugador, Arma, Combate


# Create your views here.

#Inicio

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

# Registro

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
    template_name = 'app/estadisticas.html'



@login_required
def combate(request, combate_id):
    """
    Aquí recogemos todos los requisitos que se necesitan para efectuar un combate
    """
    combate_creado = get_object_or_404(Combate, id=combate_id)
    jugador1 = combate_creado.luchador_1
    arma_jugador1 = Arma.objects.get(id=jugador1.arma_id)
    enemigo = combate_creado.luchador_2
    veneno = None
    veneno_enemigo = None
    guardia = False

    mensaje = ""
    mensaje_accion = ""
    mensaje_estado = ""
    mensaje_estado_2 = ""
    mensaje_estado_enemigo = ""
    mensaje_estado_enemigo_2 = ""
    mensaje_enemigo = ""
    mensaje_accion_enemigo = ""
    mensaje_guardia = ""
    mensaje_dano = ""
    mensaje_mana = ""
    mensaje_adicional = ""
    mensaje_adicional_2 = ""
    derrota_j1 = ""
    derrota_enemigo = ""

    if request.method == "POST":

        accion = request.POST.get("accion")
        if accion == "atacar":
            combate_creado.turnos += 1
            combate_creado.save()
            jugador1.mana += 10
            jugador1.save()
            if chances():
                critico = arma_jugador1.dano + arma_jugador1.critico
                enemigo.salud -= critico
                mensaje = f"{jugador1.nombre} acierta un golpe certero a {enemigo.nombre}. ¡Le causa {critico} puntos de daño y recupera 10 de maná!"
            else:
                enemigo.salud -= arma_jugador1.dano
                mensaje = f"{jugador1.nombre} ataca a {enemigo.nombre}. ¡Le causa {arma_jugador1.dano} puntos de daño y recupera 10 de maná!"
            if chances():
                mensaje_adicional = f"{jugador1.nombre} ha pillado desprevenido a {enemigo.nombre}, ha logrado atacar otra vez!"
                if chances():
                    critico = arma_jugador1.dano + arma_jugador1.critico
                    enemigo.salud -= critico
                    mensaje_adicional_2 = f"{jugador1.nombre} acierta un golpe certero a {enemigo.nombre}. ¡Le causa {critico} puntos de daño y recupera 10 de maná!"
                else:
                    enemigo.salud -= arma_jugador1.dano
                    mensaje_adicional_2 = f"{jugador1.nombre} ataca a {enemigo.nombre}. ¡Le causa {arma_jugador1.dano} puntos de daño y recupera 10 de maná!"
            enemigo.save()


        elif "hb" in accion:
            combate_creado.turnos += 1
            combate_creado.save()
            opcion = accion
            mensaje = f"{jugador1.nombre} usa una habilidad especial."
            match opcion:
                case "hb1":
                    if jugador1.mana >= 50:
                        mensaje_accion = f"{jugador1.nombre} lanza una onda de energía a {enemigo.nombre} causandole 150 puntos de daño."
                        enemigo.salud -= 150
                        jugador1.mana -= 50
                        jugador1.save()
                        enemigo.save()
                    else:
                        mensaje_mana = f"{jugador1.nombre} no tiene suficiente mana para realizar su ataque, pierde su turno canalizando energía."
                        jugador1.mana += 5
                case "hb2":
                    if jugador1.mana >= 70:
                        mensaje_accion = f"{jugador1.nombre} ataca con una púa venenosa a {enemigo.nombre} causandole 120 puntos de daño."
                        enemigo.salud -= 120
                        jugador1.mana -= 70
                        jugador1.save()
                        enemigo.save()
                        rng = random.randint(0, 10)
                        if rng >= 7:
                            veneno = True
                            mensaje_estado = f"{enemigo.nombre} ha sido envenenado."
                    else:
                        mensaje_mana = f"{jugador1.nombre} no tiene suficiente mana para realizar su ataque, pierde su turno canalizando energía."
                        jugador1.mana += 5
                case "hb3":
                    if jugador1.mana >= 30:
                        mensaje_accion = f"{jugador1.nombre} se prepara para recibir el ataque."
                        guardia = True
                        jugador1.mana -= 30
                        jugador1.save()
                    else:
                        mensaje_mana = f"{jugador1.nombre} no tiene suficiente mana para realizar su ataque, pierde su turno canalizando energía."
                        jugador1.mana += 5

                case "hb4":
                    if jugador1.mana >= 100:
                        jugador1.mana -= 100
                        mensaje_accion = f"{jugador1.nombre} canaliza su energía para realizar curar sus heridas."
                        jugador1.salud += 300
                        jugador1.save()
                    else:
                        mensaje_mana = f"{jugador1.nombre} no tiene suficiente mana para realizar su ataque, pierde su turno canalizando energía."
                        jugador1.mana += 5

        if veneno:
            mensaje_estado_2 = f"{enemigo.nombre} sufre daños de envenenamiento, pierde 100 puntos de vida."
            enemigo.salud -= 100
            enemigo.save()

        if enemigo.salud <= 0:
            derrota_enemigo = f"{enemigo.nombre} ha sido derrotado, enhorabuena"
            jugador1.victorias += 1
            jugador1.save()
            enemigo.derrotas += 1
            enemigo.salud = 200
            enemigo.save()
            return render(request, "app/resolucion.html", {"combate": combate_creado, "resolucion_2": derrota_enemigo})

        if not chances():
            mensaje_enemigo = f"{enemigo.nombre} se prepara para atacar."
            if guardia:
                mensaje_guardia = f"{jugador1.nombre} ha encajado el golpe, no sufre daños."
            else:
                mensaje_dano = f"{jugador1.nombre} ha recibido el golpe, sufre {arma_jugador2.dano} puntos de daño."
                jugador1.salud -= arma_jugador2.dano
                jugador1.save()
        else:
            mensaje_enemigo = f"{enemigo.nombre} se prepara para lanzar un ataque especial."

            ataque_especial = randint(1,3)

            match ataque_especial:
                case 1:
                    mensaje_accion_enemigo = f"{enemigo.nombre} ha lanza una onda de energía a {jugador1.nombre} causandole 200 puntos de daño."
                    jugador1.salud -= 200
                    jugador1.save()
                case 2:
                    mensaje_accion_enemigo = f"{enemigo.nombre} ataca con una púa venenosa a {jugador1.nombre} causandole 120 puntos de daño."
                    jugador1.salud -= 120
                    rng = random.randint(0, 10)
                    if rng >= 7:
                        veneno_enemigo = True
                        mensaje_estado_enemigo = f"{jugador1.nombre} ha sido envenenado."
                case 3:
                    mensaje_accion_enemigo = f"{enemigo.nombre} canaliza su energía para realizar curar sus heridas, recupera 300 puntos de vida."
                    enemigo.salud += 300
                    enemigo.save()

            if veneno_enemigo:
                mensaje_estado_enemigo_2 = f"{enemigo.nombre} sufre daños de envenenamiento, pierde 100 puntos de vida."
                enemigo.salud -= 100
                enemigo.save()

        if jugador1.salud <= 0:
            derrota_j1 = f"{jugador1.nombre} ha sido derrotado, se acabó"
            enemigo.victorias += 1
            enemigo.save()
            jugador1.salud = 1
            jugador1.derrotas += 1
            jugador1.save()
            return render(request, "app/resolucion.html", {"combate": combate_creado, "resolucion_1": derrota_j1})

        return render(request, "app/combate.html", {
            "combate": combate_creado,
            "jugador1": jugador1,
            "enemigo": enemigo,
            "mensaje": mensaje,
            "mensaje_accion": mensaje_accion,
            "mensaje_adicional": mensaje_adicional,
            "mensaje_adicional_2": mensaje_adicional_2,
            "mensaje_estado": mensaje_estado,
            "mensaje_estado_2": mensaje_estado_2,
            "mensaje_guardia": mensaje_guardia,
            "mensaje_dano": mensaje_dano,
            "mensaje_enemigo": mensaje_enemigo,
            "mensaje_accion_enemigo": mensaje_accion_enemigo,
            "mensaje_estado_enemigo" : mensaje_estado_enemigo,
            "mensaje_estado_enemigo_2" : mensaje_estado_enemigo_2,
            "mensaje_mana": mensaje_mana,
        })

    return render(request, "app/combate.html", {
        "combate": combate_creado,
        "jugador1": jugador1,
        "enemigo": enemigo,
    })

def chances():
    rng = random.randint(1, 10)
    if rng == 1:
        return True
    else:
        return False