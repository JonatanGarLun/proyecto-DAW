let indiceActual = 0;

function obtenerOpciones() {
    return Array.from(document.querySelectorAll('.opcion'));
}

function actualizarSeleccion() {
    const opciones = obtenerOpciones();
    opciones.forEach((el, i) => el.classList.toggle('activa', i === indiceActual));

    const activa = opciones[indiceActual];
    const nuevaImagen = activa.dataset.img;

    // Fade to black
    const fade = document.getElementById('pantalla-fade');
    fade.style.opacity = '1';

    setTimeout(() => {
        document.getElementById('imagen-central').src = nuevaImagen;
        fade.style.opacity = '0';
    }, 700);
}

function navegarIzquierda() {
    const opciones = obtenerOpciones();
    indiceActual = (indiceActual - 1 + opciones.length) % opciones.length;
    actualizarSeleccion();
}

function navegarDerecha() {
    const opciones = obtenerOpciones();
    indiceActual = (indiceActual + 1) % opciones.length;
    actualizarSeleccion();
}

function seleccionarActual() {
    const opciones = obtenerOpciones();
    const activa = opciones[indiceActual];
    const destino = activa.dataset.url;
    window.location.href = destino;
}

function manejarTeclas(e) {
    switch (e.key) {
        case 'ArrowLeft':
            navegarIzquierda();
            break;
        case 'ArrowRight':
            navegarDerecha();
            break;
        case 'Enter':
            seleccionarActual();
            break;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    actualizarSeleccion();
    document.addEventListener('keydown', manejarTeclas);

    obtenerOpciones().forEach((opcion, i) => {
        opcion.addEventListener('click', () => {
            indiceActual = i;
            actualizarSeleccion();
        });
        opcion.addEventListener('dblclick', seleccionarActual);
    });
});
