# 🧪 Sistema de Efectos (`efectos.py`)

Este módulo gestiona todo el sistema de efectos de estado del combate: desde los clásicos buffs y debuffs hasta efectos
negativos como veneno o quemadura. También maneja la aplicación, mantenimiento, expiración y visualización de estos
efectos.

Todos los efectos se almacenan en el diccionario `stats_temporales["estados"]`, que es evaluado turno a turno para
aplicar o actualizar su impacto. Este módulo es invocado principalmente por los módulos `jugador.py`, `enemigos.py` y
`utils_resolvedor.py`.

---

## 🧬 Aplicación y mantenimiento de estados

### `aplicar_estado(stats_temporales, estado_nuevo)`

Aplica un nuevo efecto (buff, debuff o negativo) al conjunto de estadísticas temporales de un personaje.

- Evita duplicados: si un efecto similar ya existe, lo reemplaza o actualiza la duración.
- Aplica directamente el efecto si es un `buff` o `debuff` (alterando `ataque`, `defensa`, etc.).
- Los efectos `negativos` se registran, pero se activan en `procesar_estados()`.

### `procesar_estados(stats_temporales, objeto)`

Ejecuta los efectos activos:

- Los efectos `negativos` causan daño porcentual a la salud máxima.
- Los `buffs` y `debuffs` se activan si aún no lo estaban.
- Reduce en 1 la duración de cada estado.

Devuelve una lista de mensajes descriptivos para el log del combate.

### `limpiar_estados_expirados(stats_temporales)`

Elimina efectos cuya duración ha terminado y revierte sus alteraciones estadísticas.

- Buffs y debuffs restauran su efecto aplicado antes de ser eliminados.
- Los efectos expirados no se mantienen en el array de estados.

---

## ❌ Eliminación de estados

### `remover_estado(stats_temporales, tipo, identificador=None)`

Elimina un estado específico según tipo (`buff`, `debuff` o `negativo`) y su identificador (`stat` o `estado`).

- Si no se pasa `identificador`, elimina todos los estados del tipo dado.
- Útil para habilidades de purga o inmunidad.

---

## 🌀 Aplicación condicional con probabilidad

### `aplicar_efecto_contrario(efecto, stats_objetivo, objetivo, log_combate=None)`

Aplica un efecto a un objetivo solo si supera una tirada de probabilidad (`tirada()`).

- Si falla la tirada, registra en el log que el objetivo resistió el efecto.
- Si se aplica, utiliza `aplicar_estado()` y añade una descripción del resultado.

Este método centraliza la aplicación de efectos desde habilidades ofensivas o defensivas.

---

## 🧾 Visualización e inspección de efectos

### `listar_estados_activos(stats_temporales)`

Devuelve una lista con descripciones legibles de todos los estados activos del personaje.

- Efectos `negativos`: muestran nombre, daño/turno y duración.
- Buffs y debuffs: indican `stat` afectado, porcentaje o valor, y duración restante.

### `estado_activo(stats_temporales, tipo, identificador)`

Comprueba si un efecto concreto está activo.

- Identifica por `tipo` y `estado` (si es `negativo`) o `stat` (si es `buff`/`debuff`).
- Devuelve `True` si se encuentra activo, `False` en caso contrario.

---

## 🧩 Integración con el sistema de combate

Este módulo se utiliza en momentos clave del combate:

- Al aplicar efectos desde habilidades (`usar_habilidad()` o `usar_habilidad_enemigo()`).
- Al inicio de cada turno (`procesar_estados()`).
- Al finalizar el turno (`limpiar_estados_expirados()`).
- Al generar descripciones visuales (`listar_estados_activos()`).

Cada efecto se maneja como un diccionario estructurado con claves como `tipo`, `stat`, `valor`, `duracion`, `porcentaje`
y `estado`.

---

## 🧠 Conclusión

El módulo `efectos.py` permite una implementación robusta y extensible del sistema de estados, crucial para añadir
profundidad estratégica al combate. Controla todo el ciclo de vida de los efectos y ofrece interfaces claras para
aplicarlos, activarlos y revertirlos.





