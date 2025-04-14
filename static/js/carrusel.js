const clases = [
    {
        nombre: "Arquero",
        imagen: "/static/resources/Pixelarts/arquero/arquero_base.png",
        descripcion: "El Arquero domina la agilidad y el daño técnico. Gracias a su altísima probabilidad de esquivar y a su velocidad, puede evitar la mayoría de los golpes enemigos y responder con ataques certeros, incluso ataques especiales adicionales. Cuanto más tiempo pasa en combate, más fuerte se vuelve, acumulando bonificaciones ofensivas y probabilidad de crítico. Es la clase perfecta para jugadores que disfrutan de un estilo de juego rápido, esquivo y demoledor a largo plazo."
    },
    {
        nombre: "Espiritualista",
        imagen: "/static/resources/Pixelarts/espiritualista/Espiritualista_base.png",
        descripcion: "El Espiritualista es el maestro de la energía y la transformación espiritual. Aumenta rápidamente su poder si gestiona bien su energía, y reacciona con mejoras significativas cada vez que es atacado. A mitad del combate se vuelve más difícil de derribar, puede ejecutar críticos letales y tiene acceso a una defensa casi impenetrable si es presionado por habilidades especiales. Una clase ideal para soporte ofensivo o duelos técnicos, donde el jugador debe leer al enemigo y contraatacar con precisión mística."
    },
    {
        nombre: "Guerrero",
        imagen: "/static/resources/Pixelarts/guerrero/guerrero_base.png",
        descripcion: "El Guerrero es un coloso imparable, diseñado para resistir el daño más brutal y devolverlo con fuerza multiplicada. Su defensa es descomunal desde el primer turno, y cada golpe que recibe lo hace más fuerte. Cuanto más tiempo permanezca en combate, más crítico y ataque acumula, convirtiéndose en una muralla ofensiva impenetrable. Ideal para los jugadores que disfrutan aguantar el frente, crecer por acumulación y terminar aplastando al enemigo con fuerza abrumadora."
    },
    {
        nombre: "Luchador",
        imagen: "/static/resources/Pixelarts/luchador/luchador_base.png",
        descripcion: "El Luchador es versatilidad y contundencia combinadas. Equilibrado entre ataque y defensa, puede adaptarse a la situación: realizar técnicas poderosas, defender con guardia automática y curarse cuando está al borde de la muerte. Cuanto más ataca y recibe daño, más se potencia. Es ideal para quienes disfrutan una mezcla de agresividad, resistencia y mecánicas de recuperación, con un pico de poder masivo si la energía espiritual se gestiona bien."
    },
    {
        nombre: "Mago",
        imagen: "/static/resources/Pixelarts/mago/mago_base.png",
        descripcion: "El Mago es una tormenta desatada de energía espiritual. Especializado en ataques mágicos consecutivos, lanza múltiples habilidades especiales en los primeros turnos, regenerando su energía cada ronda. Acumula poder con cada hechizo y se convierte en un verdadero cañón mágico si sobrevive más allá del turno cinco. Su pasiva le permite adaptarse y devastar todo el campo con precisión, defensa mágica y poder acumulativo."
    },
    {
        nombre: "Sangre Astral",
        imagen: "/static/resources/Pixelarts/sangre_astral/sangre_astral_base.png",
        descripcion: "Los Sangre Astral son una clase única. Débil al principio, pero con un potencial destructivo que escala con cada golpe recibido y ataque realizado. Gana ataques adicionales, críticos asegurados, guardia permanente y buffs masivos cuando su salud es baja. En el momento más crítico del combate, revive en su forma más poderosa, borrando los efectos negativos y reventando con un daño descomunal. Es la clase más arriesgada pero también la más recompensante del juego, ideal para jugadores que aman el riesgo extremo, las transformaciones y los finales espectaculares."
    }
];

let indiceActual = 0;

function actualizarCarrusel() {
    const total = clases.length;
    const prev = (indiceActual - 1 + total) % total;
    const next = (indiceActual + 1) % total;

    document.getElementById('prevImg').src = clases[prev].imagen;
    document.getElementById('mainImg').src = clases[indiceActual].imagen;
    document.getElementById('mainImg').setAttribute('data-clase', clases[indiceActual].nombre);
    document.getElementById('nextImg').src = clases[next].imagen;
    document.getElementById('textoClase').textContent = clases[indiceActual].descripcion;

    // Actualizar nombre debajo de la imagen
    document.getElementById('nombreClaseSeleccionada').textContent = clases[indiceActual].nombre;


    // Actualizar input hidden del formulario
    document.getElementById('id_clase').value = clases[indiceActual].nombre;

}

// Reiniciar la animación del texto
const texto = document.getElementById('textoClase');
texto.textContent = clases[indiceActual].descripcion;

function moverCarrusel(direccion) {
    const total = clases.length;
    indiceActual = (indiceActual + direccion + total) % total;
    actualizarCarrusel();
}

window.onload = actualizarCarrusel;
