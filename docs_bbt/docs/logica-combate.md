# ⚔️ Vista de Combate: `combate(request, combate_id)`

**Decoradores**: `@login_required`  
**Parámetros**:

- `request`: la solicitud del jugador.
- `combate_id`: identificador del combate actual.

La vista `combate` es el corazón del sistema jugable de Battlebound Tactics. Aquí ocurre toda la lógica de combate por
turnos entre el jugador y el enemigo. Esta vista gestiona turnos, efectos de estado, resolución de acciones,
condiciones de victoria o derrota y sincronización del estado del combate.

### Módulos

- Si desea conocer más a fondo los módulos que componen Battlebound Tactics, puede echar un vistazo a esta tabla de
  contenidos, en ella, podrás encontrar enlaces a la documentación de cada archivo

=== "🎮 Módulos del juego, dentro de `core/`"

| Módulo                                            | Descripción                                                                                                      |
|---------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
| [`jugador.py`](core-jugador.md)                   | Controla la lógica del jugador durante el combate: ataques, habilidades, energía, defensa.                       |
| [`enemigos.py`](core-enemigos.md)                 | Implementa la IA enemiga. Decide acciones según el estado del combate, controla habilidades y cooldowns.         |
| [`efectos.py`](core-efectos.md)                   | Sistema de estados: veneno, buffs, debuffs, curaciones. Aplica y gestiona sus duraciones y efectos.              |
| [`estadisticas.py`](core-estadisticas.md)         | Calcula estadísticas finales del jugador/enemigo: ataque, defensa, velocidad, etc. según nivel, pasiva y equipo. |
| [`probabilidades.py`](core-probabilidades.md)     | Define y gestiona las probabilidades de efectos como críticos, evasión, multigolpes, etc.                        |
| [`utils_combate.py`](core-utils-combate.md)       | Funciones auxiliares para interpretar efectos y habilidades. Traduce los textos a efectos aplicables.            |
| [`utils_resolvedor.py`](core-utils-resolvedor.md) | Controla la secuencia de turnos, efectos globales por turno, condiciones de victoria o derrota.                  |

---

## 🎬 Autorización y control de acceso

Al comenzar, se recupera el combate mediante su ID. Se verifica que el usuario autenticado sea el propietario del
combate. Si no lo es, se bloquea el acceso lanzando una excepción. Además, si el combate ya ha terminado, se redirige
automáticamente a la vista de resultado, para evitar que se repita o se acceda a un estado inconsistente.

---

## ⚙️ Inicialización del combate

Se inicializan las estadísticas del jugador y del enemigo a través de una función específica que calcula salud, energía,
velocidad, evasión, daño y otros modificadores. Esto incluye factores como la clase del jugador, su equipo, su nivel y
sus pasivas.

También se crea una copia temporal del estado del enemigo antes del turno. Esto servirá más adelante para saber si
recibió daño, y mostrar una animación de impacto.

---

## 💡 Aplicación de efectos al inicio del turno

Al inicio de cada turno se aplican los efectos de estado activos en cada personaje. Primero se aplican los efectos del
enemigo, otorgándole una ligera ventaja al jugador. Luego, se aplican los del jugador. Estos efectos pueden ser
beneficiosos (curación, aumentos de defensa) o perjudiciales (veneno, reducción de estadísticas).

Si alguno de los dos muere por un efecto, se detiene el flujo, se asigna una victoria o derrota al combate y se redirige
a la vista de resultado correspondiente

---

## 📥 Procesamiento de la acción del jugador

Cuando el jugador realiza una acción (por ejemplo, atacar o usar una habilidad), esta llega a través de un formulario.
Si no se detecta ninguna acción, se muestra un mensaje de error en el registro del combate.

---

## ⏱️ Prioridad por velocidad

Antes de ejecutar los turnos, se compara la estadística de velocidad del jugador y del enemigo. Quien tenga más
velocidad actúa primero. Si están empatados, el jugador tiene prioridad.

---

## 🔁 Ciclo de turnos

Dependiendo de quién actúe primero, se siguen dos posibles flujos:

### Si el jugador actúa primero:

1. El jugador realiza su acción.
2. Si el enemigo muere, el combate termina con victoria.
3. Si sigue vivo, el enemigo realiza su acción.
4. Si el jugador muere, el combate termina con derrota.

### Si el enemigo actúa primero:

1. El enemigo realiza su acción.
2. Si el jugador muere, termina en derrota.
3. Si sigue vivo, el jugador ejecuta su turno.
4. Si el enemigo muere, termina en victoria.

Este sistema garantiza que ambos personajes puedan actuar, pero da ventaja a quien tenga mayor velocidad.

---

## 💢 Detección de daño y animación

Después de ejecutar ambos turnos, se compara la salud del enemigo antes y después. Si ha cambiado, se activa una
animación visual en pantalla para indicar que ha recibido daño. Esta animación se elige aleatoriamente entre varias
disponibles, para darle dinamismo al combate.

---

## 💾 Persistencia de las estadísticas

Al final del turno, las estadísticas de ambos personajes se almacenan en sesión. También se incrementa el
contador de turnos del combate y se guarda la instancia en la base de datos. Esto asegura que, incluso si se recarga la
página, el estado actual del combate se conserva correctamente.

---

## 🧾 Renderizado de la vista

La plantilla del combate se renderiza con todos los datos relevantes:

- Estadísticas del jugador y del enemigo.
- Registro de acciones realizadas durante el turno.
- Estado del combate.
- Posibles animaciones activadas.
- Acciones disponibles para el próximo turno.

La interfaz refleja todo lo que ocurre durante la batalla, y ofrece una experiencia fluida y visualmente agradable.

---

## 📈 Funciones clave utilizadas

Esta vista depende fuertemente de funciones auxiliares, como:

- Una función para inicializar el combate. `inicializar_combate(request, combate)`
- Otra para aplicar los efectos de turno. `registrar_efecto_turno(stats_enemigo, enemigo, log)`,
  `registrar_efecto_turno(stats_jugador, jugador, log)`
- Una función dedicada al turno del jugador, que interpreta la acción y ejecuta su acción. `ejecutar_turno_jugador(request, jugador, combate, stats_jugador, stats_enemigo, enemigo, accion,
                                               log)`
- Una función similar para el enemigo, basada en una inteligencia artificial. `ejecutar_turno_enemigo(request, jugador, stats_jugador, stats_enemigo, enemigo, log,
                                               combate)`
- Funciones que resuelven el combate en caso de victoria o derrota.
  `resolver_victoria(request, jugador, enemigo, combate)`, `resolver_derrota(request, jugador, combate)`

Estas funciones están organizadas en los módulos del core (`jugador.py`, `enemigos.py`, `efectos.py`, `estadisticas.py`,
etc.) y permiten mantener la lógica bien modularizada.

---

## 🏁 Vista `resultado_combate`

Esta vista se ejecuta inmediatamente después de que el combate termina. Solo se encarga de mostrar al jugador lo que ha
ocurrido:

- Si ha ganado o perdido.
- Calcular la experiencia obtenida y si ha subido de nivel.

Se cargan todos los datos desde el modelo `Combate` y se pasan al contexto para renderizar la plantilla
`resultado.html`. Aquí no se ejecuta ninguna lógica, solo presentación.

---

## 🔄 Flujo completo del combate

[`iniciar_combate`]  
↓

[**Iniciamos las estadísticas/ las recuperamos de la sesión**]

↓

[**Aplicamos los estados del enemigo y del jugador**]  
↓

[**Comprobamos victoria o derrota**]  
↓

[**Recogemos la acción del jugador**]  
↓

[**Decidimos quien va primero según la velociadad**]  
↓

[**Ejecutamos los turnos del enemigo y el jugador**]  
↓

[**Comprobamos victoria o derrota**] ← Si nadie gana, se repite el flujo  
↓

[`resultado_combate`]

---

## 🧠 Reflexión

La vista `combate` está diseñada para ofrecer una experiencia táctica rica y detallada, donde cada decisión cuenta. Su
lógica modular permite integrar efectos complejos, decisiones de IA y estadísticas dinámicas.

Este sistema se puede ampliar fácilmente para incluir nuevas mecánicas, como habilidades pasivas avanzadas, efectos en
cadena o enemigos con fases. Es uno de los componentes más completos del proyecto, y demuestra el nivel de integración
entre frontend, backend y lógica de juego.