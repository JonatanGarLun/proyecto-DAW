# 📊 Estadísticas de Combate (`estadisticas.py`)

Este módulo centraliza el cálculo de las estadísticas del jugador y los enemigos en combate. Se encarga de combinar los
valores base con bonificaciones por pasiva, equipamiento y otros factores contextuales para producir los valores
temporales que se usan en cada turno.

También ofrece utilidades para ajustar salud y energía, mantener la proporción de estado entre combates, y generar
pasivas aleatorias al registrar un nuevo jugador.

---

## 🧱 Inicialización de estadísticas

### `inicializar_stats(objeto)`

Obtiene las estadísticas base de un objeto (jugador o enemigo):

- `salud_max`, `salud`, `ataque`, `defensa`, `velocidad`
- Si el objeto tiene energía espiritual (`jugador`), añade también `energia_max` y `energia`

Este es el punto de partida de todos los cálculos estadísticos posteriores.

---

## 🧬 Bonificadores de pasiva

### `aplicar_pasiva(jugador, stats)`

Aplica los efectos de la habilidad pasiva del jugador sobre las estadísticas base.

- Extrae el diccionario `efecto` de la instancia `Pasiva`
- Aumenta `salud_max`, `energia_max`, `ataque`, `defensa` y `velocidad` según porcentajes definidos en la pasiva

Este paso ocurre únicamente si el jugador tiene asignada una habilidad pasiva, que por defecto siempre la tiene.

---

## 🛡️ Bonificadores de equipo

### `aplicar_equipo(jugador, stats)`

Aplica los modificadores que otorgan el arma y el accesorio del jugador.

- Aumenta o disminuye directamente estadísticas como `ataque`, `defensa`, `velocidad`
- Si el accesorio lo permite, añade o resta salud y energía espiritual

---

## 🧮 Composición total de estadísticas

### `calcular_stats_totales(objeto)`

Realiza la suma total de estadísticas base + pasiva + equipo.

- Internamente llama a `inicializar_stats()`, `aplicar_pasiva()` y `aplicar_equipo()` si aplican.
- Funciona tanto para jugadores como enemigos (detecta si el objeto tiene `habilidad_pasiva` o `arma`).

---

## 🔧 Ajustes proporcionales

### `ajuste_stats(objeto, stats)`

Recalcula la salud y energía actuales para ajustarlo a sus estadísticas base.

- Usa porcentajes para escalar correctamente los nuevos valores.
- Asegura que la salud y energía no se regeneren ni pierdan tras un cambio de stats.

---

## ⚙️ Wrapper principal

### `obtener_stats_temporales(objeto)`

Función clave que se invoca desde la vista `combate` para obtener las estadísticas actuales de un jugador o enemigo.

- Llama a `calcular_stats_totales()` y luego a `ajuste_stats()`.
- Devuelve un diccionario listo para usar en combate, con todos los campos relevantes.

Este método se usa justo antes de procesar un turno o acción, asegurando que se emplean las estadísticas más precisas.

---

## 🎲 Pasiva aleatoria al registrarse

### `generar_pasiva_aleatoria_jugador(jugador)`

Genera una instancia de `Pasiva` única al registrar un nuevo jugador.

- Asigna valores aleatorios entre 0.0 y 1.0 a todos los campos de `efecto`
- Crea el objeto `Pasiva` en la base de datos
- Se asocia automáticamente al jugador

Este método garantiza que cada jugador inicia con una combinación pasiva única.

---

## 🧩 Relación con otros módulos

Este módulo es utilizado constantemente por:

- `jugador.py` y `enemigos.py`, para obtener estadísticas en combate.
- `views.py`, cuando se prepara el contexto de combate o se inicia una nueva sesión.
- `models.py`, al registrar jugadores y asignar pasivas.

Las estadísticas generadas son claves para que los efectos, habilidades, y daños funcionen correctamente.

---

## 🧠 Conclusión

El módulo `estadisticas.py` actúa como el núcleo de cálculo para todo lo relacionado con los atributos en combate. Su
diseño flexible permite extender fácilmente los modificadores, integrar nuevos tipos de pasivas o equipo, y mantener la
coherencia entre diferentes entidades del juego.