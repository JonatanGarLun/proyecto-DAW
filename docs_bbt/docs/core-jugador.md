# 🧙‍♂️ Lógica del Jugador (`jugador.py`)

Este módulo contiene la lógica fundamental del jugador durante el combate. Define cómo el jugador ataca, utiliza
habilidades, recibe daño, sube de nivel, gana experiencia y ejecuta su turno. Es llamado directamente desde la vista
`combate()` a través de la función `ejecutar_turno_jugador()`, lo que lo convierte en una pieza central del sistema.

---

## ⚔️ Acciones básicas del combate

### `accion_basica(stats_temporales, jugador)`

Realiza un ataque básico. Calcula el daño infligido, incluyendo si se trata de un golpe crítico.

- Si hay crítico (probabilidad determinada por `critico()`), el daño se multiplica por 2.5.
- Devuelve el daño infligido y un mensaje para el registro del combate.

### `ataque_adicional(stats, jugador)`

Intenta realizar un segundo ataque en el mismo turno si se cumple la probabilidad (`adicional()`).

- Si se activa, llama a `accion_basica()` y lo ejecuta de nuevo.
- Si no, devuelve un mensaje indicando que no fue posible continuar la ofensiva.

### `calcular_golpe_recibido(golpe, jugador, stats_temporales)`

Calcula el daño que recibe el jugador, teniendo en cuenta su defensa y probabilidad de esquivar (
`probabilidades.esquivar()`).

- Si esquiva, el daño es 0.
- Si no, el daño se reduce por defensa y se garantiza un mínimo del 0.125% de la salud máxima.

---

## ✨ Uso de habilidades

### `uso_habilidad(jugador, habilidad, stats_temporales)`

Lógica para el uso de habilidades activas (habilidad_1, 2 o 3).

- Verifica si el jugador tiene energía y salud suficiente para ejecutar la habilidad.
- Aplica el coste correspondiente.
- Interpreta el efecto (daño, curación, buff, debuff) usando `leer_efecto()` y `aplicar_estado()`.
- Devuelve los efectos generados y los mensajes a mostrar en el log del combate.

---

## 🧮 Cálculos post-combate

### `actualizar_stats_finales(jugador, stats_temporales)`

Actualiza la salud y energía reales del jugador después del combate.

- Calcula los porcentajes restantes de salud y energía.
- Los aplica sobre los valores máximos del jugador para guardarlos en la base de datos.

---

## 📈 Progresión y experiencia

### `subir_nivel(jugador, nuevo_nivel)`

Incrementa el nivel del jugador y escala sus estadísticas según su clase.

- Aplica una curva base y un multiplicador por nivel y clase.
- Aumenta salud máxima, energía espiritual, ataque, defensa y velocidad.

### `obtener_incremento_exp_por_nivel(nivel)`

Devuelve el porcentaje de incremento de la experiencia máxima por nivel según el rango de niveles:

- 0.05 hasta nivel 25
- 0.08 hasta nivel 50
- 0.12 hasta nivel 80
- 0.15 hasta nivel 120
- 0.20 a partir de ahí

### `ganar_experiencia(jugador, exp_ganada)`

Añade experiencia al jugador y maneja las subidas de nivel si se supera el máximo.

- Utiliza `subir_nivel()` y `obtener_incremento_exp_por_nivel()`.
- Devuelve un log con mensajes de experiencia ganada y niveles alcanzados.

---

## 🔁 Ejecución del turno del jugador

### `ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion, log)`

Esta función es llamada desde la vista `combate()` cuando el jugador realiza una acción.

- **"atacar"**: Ejecuta `accion_basica()`, aplica el daño al enemigo, y ,si se activa, realiza un `ataque_adicional()`.
- **"habilidad_1", "habilidad_2", "habilidad_3"**: Llama a `uso_habilidad()` y procesa sus efectos.
- **"huir"**: Termina el combate como derrota para el jugador con `resolver_derrota()`.
- **"pasar"**: El jugador no actúa y recupera un pequeño porcentaje de salud.

- Todos los efectos se anotan en el `log`, y se comprueba si el enemigo ha sido derrotado para llamar a
  `resolver_victoria()`.

---

## 🧩 Relación con la vista `combate()`

La función `ejecutar_turno_jugador()` es invocada directamente en la vista `combate()` cuando el jugador envía un `POST`
con una acción. Es el punto de entrada de toda interacción del jugador en combate y delega internamente en el resto de
funciones del módulo.

## Fragmento relevante en `views.py`:

#### `resultado = ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion, log)`

---

## 🧠 Conclusión

Este módulo representa el comportamiento completo del jugador en combate. Desde sus ataques básicos y habilidades hasta
su evolución y progresión por niveles. Todas las funciones están integradas en la vista de combate y definen la
experiencia jugable del jugador desde el punto de vista de la lógica del servidor.
