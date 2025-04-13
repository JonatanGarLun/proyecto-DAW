const clases = [
    {
        nombre: "Arquero",
        imagen: "/static/resources/Pixelarts/arquero/arquero_base.png",
        descripcion: "Legado: Errantes del Viento\n" +
            "Los Arqueros son herederos de los Vigías del Horizonte, exploradores del reino de Kharun. Expertos en detectar amenazas antes de que golpeen. Fueron acusados de traición y exiliados al desierto, donde su estilo de vida nómada se perfeccionó.\n" +
            "Entre tormentas de arena y ruinas perdidas, los Errantes fueron acogidos por los Espiritualistas, quienes les enseñaron el arte de leer el flujo del viento y la energía. De esta mezcla nació su estilo de “meditación en movimiento”.\n" +
            "Desconfían de los Guerreros, a quienes acusan de abandono. Admiran a los Luchadores, pero no comprenden su brutalidad. Han trabajado ocasionalmente con los Magos, quienes valoran sus mapas y textos antiguos, aunque sin formar lazos duraderos.\n" +
            "Con los Sangre Astral no tienen relación directa, pero algunos Arqueros nómadas sirvieron como guías para los jóvenes portadores de esta sangre celestial durante sus despertares."
    },
    {
        nombre: "Espiritualista",
        imagen: "/static/resources/Pixelarts/espiritualista/Espiritualista_base.png",
        descripcion: "Legado: Orden del Manantial\n" +
            "Nacidos del silencio, de la observación y de la conexión con el mundo invisible, los Espiritualistas canalizan la energía del Río Interior, un manantial espiritual que fluye entre todos los seres vivos.\n" +
            "Fueron aliados cercanos de los Magos, hasta que estos provocaron el colapso del Relicario. Hoy, solo queda un respeto antiguo, pero las heridas siguen abiertas.\n" +
            "Son los únicos que han mantenido lazos fuertes con los Arqueros, compartiendo entrenamiento en silencio y entendimiento espiritual en movimiento. A los Guerreros los han sanado. A los Luchadores, los han rechazado.\n" +
            "Esta rivalidad con los Luchadores es antigua y constante: dos filosofías enfrentadas. Dos caminos válidos, pero opuestos.\n" +
            "Los Sangre Astral, por su parte, representan caos puro. Les temen, pero también les compadecen, pues saben que su alma está en guerra."
    },
    {
        nombre: "Guerrero",
        imagen: "/static/resources/Pixelarts/guerrero/guerrero_base.png",
        descripcion: "Legado: Los Bastiones de Kharun\n" +
            "Los Guerreros provienen del antiguo reino de Kharun, una civilización amurallada cuyo ejército estaba forjado en piedra, metal y juramentos de honor. Su función era proteger, resistir, jamás ceder. Criados dentro de fortalezas que tocaban el cielo, su entrenamiento se enfocaba en la disciplina, la resistencia y la entrega total a la defensa del mundo.\n" +
            "Kharun no solo tenía soldados. También poseía una élite de exploradores conocidos como los Vigías del Horizonte —los antepasados de los Arqueros— quienes fueron acusados falsamente de traición y exiliados, una fractura que nunca sanó.\n" +
            "Los Magos, guardianes del saber, consideraban a los Guerreros como brutos útiles. A su vez, los Guerreros veían la magia como inestable, peligrosa si no se controla. No obstante, colaboraron en la defensa de las ruinas del Relicario Eterno, una unión forzada que aún genera desconfianza mutua.\n" +
            "Con los Luchadores, existe una especie de respeto tácito. Un Guerrero legendario salvó a uno durante una invasión, dando inicio a una leyenda conocida por ambas clases. Pero los Guerreros siguen el orden; los Luchadores, el pueblo. Es una diferencia que marca."
    },
    {
        nombre: "Luchador",
        imagen: "/static/resources/Pixelarts/luchador/luchador_base.png",
        descripcion: "Legado: Camino de los Puños Rojos\n" +
            "Nacidos del hambre, la injusticia y la rabia contenida, los Luchadores no vienen de linajes nobles. Son hijos del pueblo, entrenados entre ruinas y callejones. Creen que el verdadero poder no se hereda: se sangra.\n" +
            "Desde su inicio, han rechazado los templos, las órdenes y las murallas. Su filosofía choca directamente con la de los Espiritualistas, quienes creen en el equilibrio. Para un Luchador, la contemplación es inacción. Para un Espiritualista, la furia descontrolada es ruina.\n" +
            "Sin embargo, los Luchadores admiran en secreto a los Guerreros por su coraje, y sienten una conexión especial con los Sangre Astral, que luchan contra sí mismos como ellos luchan contra el mundo.\n" +
            "Los Magos les resultan innecesariamente complejos, y con los Arqueros mantienen una distancia de mutuo respeto."
    },
    {
        nombre: "Mago",
        imagen: "/static/resources/Pixelarts/mago/mago_base.png",
        descripcion: "Legado: Custodios del Relicario Eterno\n" +
            "Los Magos fueron alguna vez los protectores del conocimiento universal a través del Relicario Eterno, una biblioteca viviente de energía pura que contenía almas, sabiduría y futuro. Cuando fue fragmentado, los Magos se dividieron: algunos querían reconstruirlo, otros sellarlo para siempre.\n" +
            "Colaboraron antaño con los Espiritualistas, con quienes compartían conocimientos del alma. Pero esa alianza se rompió tras la caída del Relicario, que desequilibró todo el plano espiritual.\n" +
            "El surgimiento de los Sangre Astral tras la caída de un meteorito repleto de energía pura representa, para ellos, un error cósmico. Los Magos los consideran inestables, peligrosos. Han intentado sellar su poder más de una vez.\n" +
            "También han chocado con los Guerreros, que protegieron ruinas del Relicario sin permiso. Aunque los usan como protectores temporales, no los consideran iguales.\n" +
            "Utilizan textos perdidos de los Errantes del Viento (Arqueros), lo cual ha generado una cooperación distante pero respetuosa."
    },
    {
        nombre: "Sangre Astral",
        imagen: "/static/resources/Pixelarts/sangre_astral/sangre_astral_base.png",
        descripcion: "Legado: Hijos de la Nova\n" +
            "Durante un eclipse triple, siete meteoritos cayeron sobre el mundo, trayendo consigo la energía viva del cosmos. Quienes sobrevivieron al impacto fueron transformados: cuerpos más fuertes, almas en llamas, y una furia incontrolable. Nacieron los Sangre Astral.\n" +
            "No eligieron este destino, y por eso muchos vagan buscando propósito. Han sido perseguidos por Magos, estudiados por Guerreros, y entrenados por Luchadores que comprenden el dolor de ser arma y escudo a la vez.\n" +
            "Los Espiritualistas les temen, y los Arqueros rara vez se cruzan con ellos. Pero algunos Errantes del Viento han guiado a jóvenes Sangre Astral en sus primeros años, cuando aún eran frágiles y confundidos.\n" +
            "A medida que su poder despierta, muchos Sangre Astral escuchan un llamado, una voz de entre las estrellas. Algo, o alguien, los llama a regresar al cráter del primer impacto…"
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
