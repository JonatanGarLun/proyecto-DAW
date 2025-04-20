// static/js/inicio.js

document.addEventListener("DOMContentLoaded", () => {
  const carrusel = document.getElementById("carrusel-opciones");
  const opciones = Array.from(carrusel.getElementsByClassName("opcion"));
  const flechaIzquierda = document.getElementById("flecha-izquierda");
  const flechaDerecha = document.getElementById("flecha-derecha");
  const imagenCentral = document.getElementById("imagen-central");

  let indexActivo = 0; // Opción seleccionada por defecto

  // Función para actualizar estilo visual de la opción activa
  function actualizarOpcionActiva() {
    opciones.forEach((opcion, idx) => {
      if (idx === indexActivo) {
        opcion.classList.add("opcion-activa");
      } else {
        opcion.classList.remove("opcion-activa");
      }
    });
  }

  // Función para cambiar la imagen central con fade
  function cambiarImagenCentral(nuevaImagen) {
    // fade-out
    imagenCentral.classList.add("fade-out");
    setTimeout(() => {
      // Cambiamos la src
      imagenCentral.src = nuevaImagen;
      // Removemos fade-out y agregamos fade-in
      imagenCentral.classList.remove("fade-out");
      imagenCentral.classList.add("fade-in");

      // Quitamos fade-in después de un tiempo
      setTimeout(() => {
        imagenCentral.classList.remove("fade-in");
      }, 400);
    }, 400);
  }

  // Avanzar o retroceder en el carrusel
  function moverCarrusel(direccion) {
    if (direccion === "left") {
      indexActivo = (indexActivo - 1 + opciones.length) % opciones.length;
    } else if (direccion === "right") {
      indexActivo = (indexActivo + 1) % opciones.length;
    }
    actualizarOpcionActiva();
    // Cambiar imagen central según la opción activa
    const opcionActiva = opciones[indexActivo];
    const nuevaImagen = opcionActiva.getAttribute("data-imagen-central");
    cambiarImagenCentral(nuevaImagen);
  }

  // Al hacer clic en flecha izquierda
  flechaIzquierda.addEventListener("click", () => {
    moverCarrusel("left");
  });

  // Al hacer clic en flecha derecha
  flechaDerecha.addEventListener("click", () => {
    moverCarrusel("right");
  });

  // Al hacer clic en una opción directamente
  opciones.forEach((opcion, idx) => {
    opcion.addEventListener("click", () => {
      indexActivo = idx;
      actualizarOpcionActiva();
      const nuevaImagen = opcion.getAttribute("data-imagen-central");
      cambiarImagenCentral(nuevaImagen);
    });

    // Al hacer doble clic, redirige
    opcion.addEventListener("dblclick", () => {
      const url = opcion.getAttribute("data-url");
      window.location.href = url;
    });
  });

  // Control por teclado
  document.addEventListener("keydown", (e) => {
    switch(e.key) {
      case "ArrowLeft":
        moverCarrusel("left");
        break;
      case "ArrowRight":
        moverCarrusel("right");
        break;
      case "Enter":
        // Redirigir a la opción activa
        const opcionActiva = opciones[indexActivo];
        const url = opcionActiva.getAttribute("data-url");
        window.location.href = url;
        break;
    }
  });

  // Inicializar el carrusel
  actualizarOpcionActiva();
  // Opcional: actualizar la imagen central de inicio si deseas
  const opcionInicial = opciones[indexActivo];
  const imagenInicial = opcionInicial.getAttribute("data-imagen-central");
  imagenCentral.src = imagenInicial;
});
