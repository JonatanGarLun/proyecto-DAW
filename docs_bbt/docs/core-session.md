# 🗂️ Limpieza de Sesión de Combate (`session.py`)

Este módulo ofrece una única función: eliminar de la sesión del usuario todos los datos relacionados con un combate. 
Su propósito es garantizar que, una vez finalizado un combate (ya sea por victoria, derrota o abandono), el
sistema no conserve estadísticas temporales o indicadores de estado innecesarios.

---

## 🧹 Limpieza de sesión

### `limpiar_sesion_combate(request, combate_id)`

Elimina de la sesión del usuario todas las claves asociadas al combate con ID proporcionado.

- `stats_jugador`: estadísticas temporales del jugador.
- `stats_enemigo`: estadísticas temporales del enemigo.
- `combate_{combate_id}_iniciado`: bandera que marca si el combate ya se ha inicializado en sesión.

Utiliza `session.pop(clave, None)` para eliminar cada clave sin lanzar errores si no existe.

---

## 🧩 Relación con otros módulos

- Usado en `utils_resolvedor.py`, tanto en `resolver_victoria()` como en `resolver_derrota()` para limpiar la sesión
  tras finalizar el combate.
- Garantiza que futuros combates empiecen con una sesión limpia, evitando estados corruptos o residuales.

---

## 🧠 Conclusión

Aunque sencillo, el módulo `session.py` cumple una función crítica: limpiar adecuadamente los datos de combate en sesión
para asegurar un flujo correcto en nuevos enfrentamientos. Esta limpieza ayuda a mantener la integridad del sistema de
combate entre partidas.





