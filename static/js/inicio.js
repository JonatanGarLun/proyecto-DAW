document.addEventListener("DOMContentLoaded", () => {
    const carrusel = document.getElementById("carrusel-opciones");
    const opciones = Array.from(carrusel.getElementsByClassName("opcion"));
    const flechaIzquierda = document.getElementById("flecha-izquierda");
    const flechaDerecha = document.getElementById("flecha-derecha");
    const fondo = document.getElementById("fondo-dinamico");
    const overlay = document.getElementById("fade-overlay");

    if (!fondo || !overlay) {
        console.error("No se encontró el fondo dinámico o el overlay.");
        return;
    }

    let indexActivo = 0; // Opción seleccionada por defecto

    function actualizarOpcionActiva() {
        opciones.forEach((opcion, idx) => {
            if (idx === indexActivo) {
                opcion.classList.add("opcion-activa");
            } else {
                opcion.classList.remove("opcion-activa");
            }
        });
    }

    function cambiarImagenCentral(nuevaImagen) {
        if (!nuevaImagen) {
            console.warn("No se proporcionó ninguna imagen para el fondo.");
            return;
        }

        // Fade to black
        overlay.style.opacity = 1;

        setTimeout(() => {
            fondo.style.backgroundImage = `url('${nuevaImagen}')`;
            overlay.style.opacity = 0;
        }, 400);
    }

    function moverCarrusel(direccion) {
        if (direccion === "left") {
            indexActivo = (indexActivo - 1 + opciones.length) % opciones.length;
        } else if (direccion === "right") {
            indexActivo = (indexActivo + 1) % opciones.length;
        }
        actualizarOpcionActiva();
        const opcionActiva = opciones[indexActivo];
        const nuevaImagen = opcionActiva.getAttribute("data-imagen-central");
        cambiarImagenCentral(nuevaImagen);
    }

    flechaIzquierda.addEventListener("click", () => {
        moverCarrusel("left");
    });

    flechaDerecha.addEventListener("click", () => {
        moverCarrusel("right");
    });

    opciones.forEach((opcion, idx) => {
        opcion.addEventListener("click", () => {
            indexActivo = idx;
            actualizarOpcionActiva();
            const nuevaImagen = opcion.getAttribute("data-imagen-central");
            cambiarImagenCentral(nuevaImagen);
        });

        opcion.addEventListener("dblclick", () => {
            const url = opcion.getAttribute("data-url");
            if (url) {
                window.location.href = url;
            }
        });
    });

    document.addEventListener("keydown", (e) => {
        switch(e.key) {
            case "ArrowLeft":
                moverCarrusel("left");
                break;
            case "ArrowRight":
                moverCarrusel("right");
                break;
            case "Enter":
                const opcionActiva = opciones[indexActivo];
                const url = opcionActiva.getAttribute("data-url");
                if (url) {
                    window.location.href = url;
                }
                break;
        }
    });

    // Inicializar carrusel
    actualizarOpcionActiva();
    const opcionInicial = opciones[indexActivo];
    const imagenInicial = opcionInicial.getAttribute("data-imagen-central");

    if (imagenInicial) {
        cambiarImagenCentral(imagenInicial);
    } else {
        console.warn("La opción inicial no tiene una imagen de fondo asignada.");
    }
});
