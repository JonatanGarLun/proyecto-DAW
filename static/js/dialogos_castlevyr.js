const frasesSecuencia = [
    "¿¡Que demonios ha pasado aquí!? ¡El reino está completamente destruido!",
    "Ese hombre... ¿Acaso ha sido él quien ha causado todo esto?",
    "¡Oye, tú! Ven aquí ahora mismo"
];

function bloquearInteraccion() {
    document.getElementById('overlay-bloqueo').style.display = 'block';
}

function desbloquearInteraccion() {
    document.getElementById('overlay-bloqueo').style.display = 'none';
}

let pasoActual = 0;

function siguienteDialogo() {
    pasoActual++;
    if (pasoActual < frasesSecuencia.length) {
        document.getElementById('texto-secuencia').innerText = frasesSecuencia[pasoActual];

    } else {
        document.getElementById('dialogo-secuencia').style.display = 'none';
        desbloquearInteraccion()
    }
}

window.addEventListener('load', function () {
    document.getElementById('jugador-img').src = imagenesJugador[claseJugador] || RUTA_DEFAULT;
    document.getElementById('texto-secuencia').innerText = frasesSecuencia[0];
    document.getElementById('dialogo-secuencia').style.display = 'flex';
    document.getElementById('nombre-dialogo-secuencia').innerText = nombreJugador;
    bloquearInteraccion();
});

// Diálogo con Havva Skript
const dialogos = [
    {quien: 'abuelo', texto: "Ah, por fin te has dignado a aparecer por aquí..."},
    {quien: 'jugador', texto: "¿Quién rayos eres tú? ¿¡Qué haces aquí!?"},
    {
        quien: 'abuelo',
        texto: "Hmph, quizás te suene el nombre Havva Skript. Soy el antiguo gobernador de estas tierras."
    },
    {quien: 'jugador', texto: "¡Imposible! Habías sido desterrado al mundo Oscuro, no puedes estar aquí"},
    {
        quien: 'abuelo',
        texto: "¿De verdad creías que iba caer tan fácilmente? No... ¡Y he vuelto para vengarme!"
    },
    {quien: 'jugador', texto: "Mientras yo siga en pie, haré todo lo posible para detenerte."},
    {
        quien: 'abuelo',
        texto: "Los guerreros que han osado desafiarme ya han fracasado... y tú no serás la excepción "
    },
    {quien: 'jugador', texto: "Hablas demasiado para ser un abuelo, acabaré contigo en un instante."},
    {
        quien: 'abuelo',
        texto: "¡JA! Por favor, no me hagas reir... En fin, dejémonos de cháchara, última oportunidad, joven ¿Estás preparado?"
    }
];

let pasoHavva = 0;

function iniciarDialogoHavva() {
    pasoHavva = 0;
    mostrarDialogoHavva();
}

const imagenJugador = imagenesJugador[claseJugador] || RUTA_DEFAULT;

function mostrarDialogoHavva() {
    const dialogo = dialogos[pasoHavva];
    if (!dialogo) {
        document.getElementById('dialogo-havva').style.display = 'none';
        abrirModal('modal-combate');
        return;
    }

    const img = dialogo.quien === 'abuelo' ? RUTA_ABUELO : imagenJugador;
    const nombre = dialogo.quien === 'abuelo' ? "Havva Skript" : nombreJugador;

    document.getElementById('imagen-dialogo-havva').src = img;
    document.getElementById('texto-dialogo-havva').innerText = dialogo.texto;
    document.getElementById('nombre-dialogo-havva').innerText = nombre;
    document.getElementById('dialogo-havva').style.display = 'flex';
    bloquearInteraccion()
}

function siguienteDialogoHavva() {
    pasoHavva++;
    mostrarDialogoHavva();
}

function abrirModal(id) {
    const modal = document.getElementById(id);
    const content = modal.querySelector('.modal-content');
    modal.classList.add("active", "animar-modal");
    content.classList.add("animar-modal");
    bloquearInteraccion();
    setTimeout(() => {
        modal.classList.remove("animar-modal");
        content.classList.remove("animar-modal");
    }, 400);
}

function cerrarModal(id) {
    const modal = document.getElementById(id);
    const content = modal.querySelector('.modal-content');
    modal.classList.add("cerrar-animacion");
    content.classList.add("cerrar-animacion");
    setTimeout(() => {
        modal.classList.remove("active", "cerrar-animacion");
        content.classList.remove("cerrar-animacion");
        desbloquearInteraccion();
    }, 300);
}