# 👾 Lógica del Enemigo (`enemigos.py`)

Este módulo define el comportamiento de los enemigos durante un combate. Contiene tanto la inteligencia artificial que
decide sus acciones como la ejecución de ataques, habilidades, efectos y cooldowns. Es el contrapunto directo del módulo
`jugador.py`, y su función principal `ejecutar_turno_enemigo()` es llamada desde la vista `combate()` para resolver el
turno del enemigo.

---

## ⚔️ Acciones básicas del enemigo

### `accion_basica_enemigo(stats_enemigo, enemigo, nivel_jugador)`

Realiza un ataque estándar del enemigo, escalado por su nivel y comparado con el del jugador.

- Aplica un golpe base y lo amplifica en función del nivel del enemigo y el del jugador.
- Puede ser un golpe crítico, lo que dobla el daño infligido (`critico()`).
- Devuelve el daño y un mensaje temático.

### `ataque_adicional_enemigo(stats_enemigo, enemigo, nivel_jugador)`

Intenta ejecutar un segundo ataque si la probabilidad lo permite (`adicional()`).

- Si tiene éxito, repite `accion_basica_enemigo()`.
- Si no, genera un mensaje narrativo sin infligir daño adicional.

### `calcular_golpe_recibido_enemigo(golpe, enemigo, stats_temporales)`

Calcula el daño que el enemigo recibe al ser atacado por el jugador.

- Considera defensa y evasión (`esquivar()`).
- Establece un daño mínimo del 1% de la salud máxima.

---

## 🔁 Cooldowns

### `reducir_cooldowns(combate)`

Reduce en 1 todos los cooldowns activos de habilidades enemigas.

- Se ejecuta al inicio del turno del enemigo.
- Guarda los nuevos valores en la instancia `Combate`.

### `cooldown_disponible(habilidad, combate)`

Verifica si una habilidad enemiga está lista para ser usada (cooldown en 0).

### `aplicar_cooldown(habilidad, combate)`

Registra el cooldown de una habilidad usada, extraído de su efecto, y lo almacena en el combate.

---

## ✨ Uso de habilidades enemigas

### `usar_habilidad_enemigo(habilidad, stats_enemigo, stats_jugador, enemigo, jugador, log)`

Ejecuta el efecto de una habilidad enemiga. Interpreta el tipo del efecto usando `leer_efecto()` y aplica sus
consecuencias:

- **Daño**: basado en el ataque del enemigo.
- **Curación**: restauración de salud en base a salud máxima.
- **Buff/Debuff/Negativo**: genera y aplica un estado con `aplicar_efecto_contrario()`.

Devuelve una lista de efectos (`daño`, `curacion`, `estado`) y un mensaje para el log del combate.

---

## 🧠 IA enemiga

### `ia_enemiga(stats_enemigo, stats_jugador, habilidades_disponibles)`

Decide qué acción tomará el enemigo en su turno, asignando pesos a cada opción:

- Evalúa salud propia y del jugador, estados activos y diferencias estadísticas.
- Usa `evaluar_buff_o_debuff()` para asignar prioridades a efectos estratégicos.
- Siempre añade la opción de ataque básico con peso bajo.

Devuelve una elección aleatoria ponderada (habilidad o `"basico"`).

### `evaluar_buff_o_debuff(tipo, stat_objetivo, stats_enemigo, stats_jugador)`

Asigna un peso de prioridad a buffs o debuffs dependiendo de las diferencias estadísticas entre jugador y enemigo.

- Si la estadística del enemigo es inferior a la del jugador, prioriza su uso.
- Se usa solo internamente por `ia_enemiga()`.

---

## 🧪 Ejecución del turno enemigo

### `ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log, combate)`

Función principal que resuelve el turno completo del enemigo. Es llamada desde la vista `combate()`.

- **Inicio**: reduce cooldowns con `reducir_cooldowns()`.
- **Decisión**: selecciona acción con `ia_enemiga()`.
- **Acción básica**: ejecuta `accion_basica_enemigo()` y posible `ataque_adicional_enemigo()`.
- **Habilidad**: usa `usar_habilidad_enemigo()`, aplica efectos, estados y cooldowns.

Al final del turno, comprueba si el jugador ha sido derrotado y llama a `resolver_derrota()` si procede.

---

## 🧩 Relación con la vista `combate()`

La vista `combate()` invoca `ejecutar_turno_enemigo()` para resolver la respuesta del enemigo

## Fragmento en `views.py`:

#### `resultado = ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log, combate)`

Esto asegura que cada combate siga una secuencia completa: jugador → enemigo (o enemigo → jugador, si el enemigo es más
rápido).

---

## 🧠 Conclusión

El módulo `enemigos.py` representa la inteligencia y ejecución de la lógica de los enemigos. Controla sus decisiones,
gestiona sus habilidades y permite una respuesta dinámica y estratégica dentro del sistema de combate. Su diseño modular
permite una IA flexible y adaptativa en función del contexto del combate.