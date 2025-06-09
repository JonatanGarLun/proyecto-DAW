# 🧩 Resolución de Turnos y Combates (`utils_resolvedor.py`)

Este módulo orquesta las transiciones globales de cada combate: desde la inicialización de los datos hasta la aplicación
de efectos y la resolución de victorias o derrotas. Actúa como un controlador lógico que mantiene la integridad del
combate turno a turno, manipulando el estado de la sesión, aplicando efectos y finalizando el combate cuando
corresponde.

Su diseño mantiene el flujo general del combate separado de la lógica de ataque o habilidad, facilitando una estructura
más modular.

---

## ⚙️ Inicialización de combate

### `inicializar_combate(request, combate)`

Carga las estadísticas temporales de jugador y enemigo en la sesión si aún no han sido inicializadas.

- Usa la función `obtener_stats_temporales()` desde `estadisticas.py`.
- Guarda las estadísticas bajo las claves `"stats_jugador"` y `"stats_enemigo"` en la sesión del usuario.
- Marca la sesión como iniciada con la clave `"combate_{id}_iniciado"`.

Este paso es esencial para que todas las operaciones posteriores (ataques, efectos, etc.) trabajen con un estado
aislado y modificable turno a turno.

---

## ☠️ Aplicación de efectos por turno

### `registrar_efecto_turno(stats_obj, objeto, log)`

Aplica los efectos de estado que estén activos y registra los resultados en el log del combate.

- Llama a `procesar_estados()` para aplicar efectos (venenos, regeneraciones, etc.).
- Luego, invoca `limpiar_estados_expirados()` para remover efectos cuya duración haya terminado.
- Todos los mensajes generados se agregan al `log`.

Este método se ejecuta al inicio del turno para mantener el sistema de efectos sincronizado con el flujo del combate.

---

## 🏆 Resolución de victoria

### `resolver_victoria(request, jugador, enemigo, combate)`

Finaliza el combate declarando al jugador como vencedor.

- Actualiza los valores definitivos del jugador con `actualizar_stats_finales()`.
- Cambia el estado del combate: `terminado = True`, `resultado = "victoria"`.
- Otorga experiencia al jugador con `ganar_experiencia()`.
- Elimina los datos de combate de la sesión con `limpiar_sesion_combate()`.
- Aumenta el contador de victorias del jugador.
- Redirige al usuario a la vista `resultado_combate`.

---

## 💀 Resolución de derrota

### `resolver_derrota(request, jugador, combate)`

Finaliza el combate indicando que el jugador ha perdido.

- Similar a `resolver_victoria()`, pero sin otorgar experiencia.
- Marca `resultado = "derrota"` y aumenta las derrotas del jugador.
- Limpia sesión y redirige al resultado del combate.

---

## 🧩 Relación con otros módulos

- Invocado desde `views.py` y `combate.py`, principalmente tras evaluar los efectos de cada acción.
- Depende de funciones de los módulos:
    - `estadisticas.py` para las estadísticas temporales
    - `efectos.py` para el manejo de estados
    - `jugador.py` para la experiencia y resultados
    - `session.py` para la limpieza de datos de combate

---

## 🧠 Conclusión

El módulo `utils_resolvedor.py` centraliza la lógica del flujo de combate en torno a la sesión, efectos y finalización.
Gracias a su estructura, garantiza un control coherente del estado global del combate, separando responsabilidades entre
los módulos de acción y el sistema de control general.