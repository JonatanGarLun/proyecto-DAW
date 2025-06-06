let dialogoBloqueado = false;

function abrirModal(id) {
    const modal = document.getElementById(id);
    const content = modal.querySelector('.modal-content');
    const dialogoVisible = document.getElementById("dialogo-thalendor").style.display === "flex";
    if (dialogoVisible) return;

    modal.classList.add("active", "animar-modal");
    content.classList.add("animar-modal");

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
    }, 300);
}

function mostrarDialogo() {
    if (dialogoBloqueado) return;

    dialogoBloqueado = true;

    const frases = [
        "No queremos a extraños en Thalendor!",
        "Una mente entrenada es más poderosa que cualquier arma.",
        "Cuidado con lo que acecha entre las sombras, nunca se sabe cuando un enemigo puede estar observando.",
        "El rey Havva Eskript fue desterrado por reinar como un tirano, fue mandado a la dimensión oscura para toda la eternidad",
        "Muchos hablan de que el rey Havva Eskript era bastante poderoso y que era uno de los mejores luchadores de todos los tiempos, aunque la última vez que fue visto estaba bastante mayor.",
        "Se dice que el reino del este enfadó a un poderoso hechizero y éste lo congeló como castigo.",
        "Las ruinas antiguas esconden secretos que nadie debería despertar.",
        "Tendrás que ser fuerte para lo que viene, joven aventurero.",
        "Esos Duendes Chillones son muy débiles, hasta un crío podría derrotar a uno.",
        "Recuerda tener tus armas y equipo al día, nunca se está suficiente preparado.",
        "El puente que conectaba nuestro reino con el reino del sur ha caído, no hay manera de acceder a él de momento",
        "Se dice que grandes desafios aguardan en el reino volcánico, pero yo no estoy dispuesto a comprobarlo.",
        "¿Qué crees que se encuentre en el castillo tenebroso, quién habrá decidido colocarlo ahí?",

    ];

    const frase = frases[Math.floor(Math.random() * frases.length)] || frases[0];
    const imagen = imagenes[Math.floor(Math.random() * imagenes.length)] || imagenes[0];

    document.getElementById("texto-dialogo").innerText = frase;
    document.getElementById("npc-imagen").src = imagen;
    document.getElementById("dialogo-thalendor").style.display = "flex";

    setTimeout(() => {
        dialogoBloqueado = false;
    }, 3000);
}

function cerrarDialogo() {
    dialogoBloqueado = false;
    document.getElementById("dialogo-thalendor").style.display = "none";
}