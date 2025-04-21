const clases = [
    {
        nombre: "Arquero",
        imagen: "/static/resources/Pixelarts/Arquero/Arquero_base.png",
        descripcion: "La Sombra certera\n" +
            "Nadie escapa de su arco, y nadie lo alcanza.\n" +
            "🏹 “Si puedes verlo, ya es tarde.”\n\n" + "El Arquero domina la agilidad y el daño técnico. Gracias a su altísima probabilidad de esquivar y a su velocidad, puede evitar la mayoría de los golpes enemigos y responder con ataques certeros, incluso ataques especiales adicionales. Cuanto más tiempo pasa en combate, más fuerte se vuelve, acumulando bonificaciones ofensivas y probabilidad de crítico. Es la clase perfecta para jugadores que disfrutan de un estilo de juego rápido, esquivo y demoledor a largo plazo."
    },
    {
        nombre: "Espiritualista",
        imagen: "/static/resources/Pixelarts/Espiritualista/Espiritualista_base.png",
        descripcion: "El Eco del Alma\n" +
            "Convierte el dolor en fuerza y la calma en poder.\n" +
            "🌫️ “Donde otros caen, yo me elevo.”\n\n" +
            "El Espiritualista es el maestro de la energía y la transformación espiritual. Aumenta rápidamente su poder si gestiona bien su energía, y reacciona con mejoras significativas cada vez que es atacado. A mitad del combate se vuelve más difícil de derribar, puede ejecutar críticos letales y tiene acceso a una defensa casi impenetrable si es presionado por habilidades especiales. Una clase ideal para soporte ofensivo o duelos técnicos, donde el jugador debe leer al enemigo y contraatacar con precisión mística."
    },
    {
        nombre: "Guerrero",
        imagen: "/static/resources/Pixelarts/Guerrero/Guerrero_base.png",
        descripcion: "El Muro Imparable\n" +
            "Una fuerza bruta que aumenta con cada golpe recibido.\n" +
            "🗡️ “Cuando el hierro sangra, la guerra empieza.”\n\n" +
            "El Guerrero es un coloso imparable, diseñado para resistir el daño más brutal y devolverlo con fuerza multiplicada. Su defensa es descomunal desde el primer turno, y cada golpe que recibe lo hace más fuerte. Cuanto más tiempo permanezca en combate, más crítico y ataque acumula, convirtiéndose en una muralla ofensiva impenetrable. Ideal para los jugadores que disfrutan aguantar el frente, crecer por acumulación y terminar aplastando al enemigo con fuerza abrumadora."
    },
    {
        nombre: "Luchador",
        imagen: "/static/resources/Pixelarts/Luchador/Luchador_base.png",
        descripcion: "El Puño del Equilibrio y la justicia\n" +
            "Golpea, resiste y se levanta una vez más.\n" +
            "💥 “Mi cuerpo es mi escudo. Mis puños, mi destino.”\n\n" +
            "El Luchador es versatilidad y contundencia combinadas. Equilibrado entre ataque y defensa, puede adaptarse a la situación: realizar técnicas poderosas, defender con guardia automática y curarse cuando está al borde de la muerte. Cuanto más ataca y recibe daño, más se potencia. Es ideal para quienes disfrutan una mezcla de agresividad, resistencia y mecánicas de recuperación, con un pico de poder masivo si la energía espiritual se gestiona bien."
    },
    {
        nombre: "Mago",
        imagen: "/static/resources/Pixelarts/Mago/Mago_base.png",
        descripcion: "El Tormento Arcano\n" +
            "Un canal de magia pura que se desborda con cada hechizo.\n" +
            "✨ “El maná fluye, el mundo tiembla.”\n\n" +
            "El Mago es una tormenta desatada de energía espiritual. Especializado en ataques mágicos consecutivos, lanza múltiples habilidades especiales en los primeros turnos, regenerando su energía cada ronda. Acumula poder con cada hechizo y se convierte en un verdadero cañón mágico si sobrevive más allá del turno cinco. Su pasiva le permite adaptarse y devastar todo el campo con precisión, defensa mágica y poder acumulativo."
    },
    {
        nombre: "Astral",
        imagen: "/static/resources/Pixelarts/Astral/Astral_base.png",
        descripcion: "El Renacido del cosmos\n" +
            "Cuanto más cerca de la muerte, más cerca de su verdad.\n" +
            "🔥 “No me has vencido… solo has despertado mi verdadero yo.”\n\n" +
            "Los Sangre Astral son una clase única. Débil al principio, pero con un potencial destructivo que escala con cada golpe recibido y ataque realizado. Gana ataques adicionales, críticos asegurados, guardia permanente y buffs masivos cuando su salud es baja. En el momento más crítico del combate, revive en su forma más poderosa, borrando los efectos negativos y reventando con un daño descomunal. Es la clase más arriesgada pero también la más recompensante del juego, ideal para jugadores que aman el riesgo extremo, las transformaciones y los finales espectaculares."
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
    const clase = clases[indiceActual].nombre;
    document.getElementById('nombreClaseSeleccionada').textContent = clase.charAt(0).toUpperCase() + clase.slice(1).toLowerCase();

    // Actualizar nombre debajo de la imagen


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
