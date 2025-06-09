# 🛠️ Utilidades de Combate (`utils_combate.py`)

Este módulo proporciona funciones auxiliares para interpretar los efectos de las habilidades tanto de jugadores como de
los enemigos. Su objetivo es abstraer el acceso a los datos del campo `efecto` y garantizar que siempre se pueda obtener
una representación unificada.

Estas utilidades son fundamentales para que módulos como `jugador.py`, `enemigos.py` o `efectos.py` puedan trabajar con
habilidades sin preocuparse por su estructura interna.

---

## 📥 Interpretación de efectos individuales

### `leer_efecto(habilidad, campo, default=None)`

Devuelve el valor de un campo específico desde el atributo `efecto` de una habilidad.

- Si la habilidad pertenece a un **jugador**, extrae directamente el diccionario `habilidad.efecto`.
- Si la habilidad es de un **enemigo**, accede a `habilidad.efecto`.
- Si el campo no existe o el formato es incorrecto, devuelve `default`.

🔍 Este método es útil para acceder a campos como `"tipo"`, `"stat"`, `"valor"`, `"porcentaje"` o `"duracion"` desde
cualquier habilidad.

---

## 🧪 Interpretación de efectos múltiples

### `leer_efectos(habilidad)`

Devuelve una **lista de efectos** aplicables desde una habilidad.

- Si el campo `efecto` es una **lista**, la retorna tal cual.
- Si es un **diccionario con clave `efectos`**, retorna el contenido de esa clave.
- Si es un **diccionario simple**, lo envuelve en una lista.
- Si no hay efectos reconocibles, devuelve una lista vacía.

✅ Este método garantiza que cualquier habilidad —por simple o compleja que sea— pueda ser tratada como una lista de
efectos en el sistema de combate.

---

## 🧩 Relación con otros módulos

- En `jugador.py` y `enemigos.py`, estas funciones son invocadas desde `usar_habilidad()` y `usar_habilidad_enemigo()`,
  respectivamente.
- En `efectos.py`, los efectos devueltos por `leer_efectos()` son aplicados con `aplicar_estado()` o
  `aplicar_efecto_contrario()`.

---

## 🧠 Conclusión

El módulo `utils_combate.py` aporta una capa de compatibilidad y uniformidad al tratamiento de habilidades en el
combate. Gracias a estas funciones, el sistema es capaz de manejar habilidades con estructuras variadas sin comprometer
la robustez del flujo de combate.





