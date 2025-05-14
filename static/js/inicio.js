let bloqueoInput = true;
let indexActivo = 0;

document.addEventListener("DOMContentLoaded", () => {
    const carrusel = document.getElementById("carrusel-opciones");
    const opciones = Array.from(carrusel.getElementsByClassName("opcion"));
    const flechaIzquierda = document.getElementById("flecha-izquierda");
    const flechaDerecha = document.getElementById("flecha-derecha");
    const fondo = document.getElementById("fondo-dinamico");
    const overlay = document.getElementById("fade-overlay");

    if (!fondo || !overlay || !opciones.length) {
        console.error("No se encontró el fondo dinámico, overlay o las opciones.");
        return;
    }

    function actualizarOpcionActiva() {
        opciones.forEach((opcion, idx) => {
            opcion.classList.toggle("opcion-activa", idx === indexActivo);
        });
    }

    function cambiarImagenCentral(nuevaImagen) {
        if (!nuevaImagen) return;
        bloqueoInput = true;
        overlay.style.pointerEvents = 'auto';
        overlay.style.opacity = 1;

        const img = new Image();
        img.src = nuevaImagen;
        img.onload = () => {
            setTimeout(() => {
                fondo.style.backgroundImage = `url('${nuevaImagen}')`;
                overlay.style.opacity = 0;
                setTimeout(() => {
                    overlay.style.pointerEvents = 'none';
                    bloqueoInput = false;
                }, 400);
            }, 400);
        };
    }

    function moverCarrusel(direccion) {
        if (bloqueoInput) return;

        if (direccion === "left") {
            indexActivo = (indexActivo - 1 + opciones.length) % opciones.length;
        } else if (direccion === "right") {
            indexActivo = (indexActivo + 1) % opciones.length;
        }

        actualizarOpcionActiva();
        const nuevaImagen = opciones[indexActivo].getAttribute("data-imagen-central");
        cambiarImagenCentral(nuevaImagen);
    }

    function transicionYRedireccion(url) {
        if (!url) return;
        bloqueoInput = true;
        overlay.style.pointerEvents = 'auto';
        overlay.style.opacity = 1;

        setTimeout(() => {
            window.location.href = url;
        }, 500);
    }

    // Eventos
    flechaIzquierda.addEventListener("click", () => moverCarrusel("left"));
    flechaDerecha.addEventListener("click", () => moverCarrusel("right"));

    opciones.forEach((opcion, idx) => {
        opcion.addEventListener("click", () => {
            if (bloqueoInput) return;
            indexActivo = idx;
            actualizarOpcionActiva();
            const nuevaImagen = opcion.getAttribute("data-imagen-central");
            cambiarImagenCentral(nuevaImagen);
        });

        opcion.addEventListener("dblclick", () => {
            const url = opcion.getAttribute("data-url");
            if (url) transicionYRedireccion(url);
        });
    });

    document.addEventListener("keydown", (e) => {
        if (bloqueoInput) return;

        if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
            moverCarrusel(e.key === "ArrowLeft" ? "left" : "right");
        }

        if (e.key === "Enter") {
            const url = opciones[indexActivo].getAttribute("data-url");
            if (url) transicionYRedireccion(url);
        }
    });

    actualizarOpcionActiva();

    // Imagen inicial
    const imagenInicial = opciones[indexActivo].getAttribute("data-imagen-central");
    if (imagenInicial) {
        const img = new Image();
        img.src = imagenInicial;
        img.onload = () => {
            fondo.style.backgroundImage = `url('${imagenInicial}')`;
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.style.pointerEvents = 'none';
                bloqueoInput = false;
            }, 400);
        };
    } else {
        overlay.style.opacity = '0';
        setTimeout(() => {
            overlay.style.pointerEvents = 'none';
            bloqueoInput = false;
        }, 400);
    }
});

// ✅ Reestablecer estado al volver atrás
window.addEventListener("pageshow", () => {
    const overlay = document.getElementById("fade-overlay");
    const fondo = document.getElementById("fondo-dinamico");
    const carrusel = document.getElementById("carrusel-opciones");
    const opciones = Array.from(carrusel.getElementsByClassName("opcion"));

    if (!overlay || !fondo || !opciones.length) return;

    bloqueoInput = false;

    overlay.style.opacity = '1';
    overlay.style.pointerEvents = 'auto';

    setTimeout(() => {
        overlay.style.opacity = '0';
        setTimeout(() => {
            overlay.style.pointerEvents = 'none';
        }, 400);
    }, 50);

    const index = opciones.findIndex(op => op.classList.contains("opcion-activa"));
    indexActivo = index >= 0 ? index : 0;
    const imagen = opciones[indexActivo].getAttribute("data-imagen-central");
    if (imagen) {
        fondo.style.backgroundImage = `url('${imagen}')`;
    }
});
