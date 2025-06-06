let dialogoBloqueado = false;

function mostrarDialogo() {
    if (dialogoBloqueado) return;

    dialogoBloqueado = true;
    document.getElementById("modal-region-nevada").style.display = "block";
}

function cerrarDialogo() {
    dialogoBloqueado = false;
    document.getElementById("modal-region-nevada").style.display = "none";
}


document.addEventListener("DOMContentLoaded", () => {
    const zonaNevada = document.querySelector(".zona-roja");
    zonaNevada.addEventListener("click", (e) => {
        e.preventDefault();
        mostrarDialogo();
    });
});