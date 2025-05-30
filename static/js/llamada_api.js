let ordenActual = "nivel";

async function cargarRanking(orden = "nivel") {
    ordenActual = orden;
    document.querySelectorAll(".ranking-filtros button").forEach(btn => btn.classList.remove("active"));
    const btnAct = [...document.querySelectorAll(".ranking-filtros button")].find(b => b.textContent.toLowerCase().includes(orden));
    if (btnAct) btnAct.classList.add("active");

    const response = await fetch(`/api/jugadores/?ordering=-${orden}`);
    const data = await response.json();

    const contenedor = document.getElementById("ranking-lista");
    contenedor.innerHTML = "";

    const top5 = data.results ? data.results.slice(0, 5) : data.slice(0, 5);

    top5.forEach((jugador, index) => {
const clase = jugador.estadisticas.clase.toLowerCase();
const imagenRuta = `${rutaClases}${clase}/${clase}_victoria.png`;

        let valor = "";
        if (orden === "nivel") valor = `Nivel: ${jugador.estadisticas.nivel}`;
        if (orden === "victorias") valor = `Victorias: ${jugador.victorias} (Win Rate: ${jugador.porcentaje_victorias})`;
        if (orden === "derrotas") valor = `Derrotas: ${jugador.derrotas}`;
        if (orden === "oro") valor = `Oro: ${jugador.oro}`;

        contenedor.innerHTML += `
        <div class="jugador-card">
            <img src="${imagenRuta}" alt="${clase}">
            <div class="jugador-info">
                <h3>🥇 ${index + 1}. ${jugador.nombre_personaje} [${jugador.usuario}]</h3>
                <p>${valor}</p>
            </div>
        </div>
            `;
    });
}

window.onload = () => cargarRanking();