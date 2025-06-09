# 🎲 Sistema de Probabilidades (`probabilidades.py`)

Este módulo define todas las probabilidades que intervienen en el combate: golpes críticos, esquivas y ataques
adicionales. Permite encapsular la lógica de azar dentro de funciones claras y reutilizables, ajustadas al tipo de clase
del jugador (el enemigo tiene unos porcentajes predefinidos).

Su propósito es centralizar la aleatoriedad y personalizarla según la clase de cada combatiente, garantizando coherencia
y balance.

---

## 🧪 Tirada base

### `tirada(probabilidad)`

Realiza una tirada aleatoria según un valor entre 0.0 y 1.0.

- Usa `random()` para generar un número aleatorio.
- Devuelve `True` si el resultado cae dentro de la probabilidad pasada como parámetro.
- Internamente utilizada por todas las funciones de este módulo.

---

## 📊 Tabla de probabilidades por clase

### `obtener_probabilidades_por_clase(clase)`

Devuelve un diccionario con las probabilidades correspondientes a una clase:

- `critico`: probabilidad de golpe crítico
- `esquivar`: probabilidad de evadir un ataque
- `adicional`: probabilidad de realizar un ataque extra

### Clases definidas y sus valores:

| Clase          | Crítico | Esquivar | Adicional |
|----------------|---------|----------|-----------|
| GUERRERO       | 0.15    | 0.04     | 0.10      |
| ARQUERO        | 0.22    | 0.18     | 0.22      |
| MAGO           | 0.17    | 0.05     | 0.12      |
| LUCHADOR       | 0.16    | 0.07     | 0.14      |
| ESPIRITUALISTA | 0.18    | 0.09     | 0.13      |
| ASTRAL         | 0.20    | 0.10     | 0.18      |

Si se pasa una clase desconocida (o un enemigo), se devuelve un conjunto de probabilidades neutras por defecto (`0.10`
en cada
categoría).

---

## ⚔️ Probabilidades de combate

### `critico(objetivo)`

Determina si el ataque del objetivo resulta en un golpe crítico.

- Extrae la clase del `objetivo`, obtiene su probabilidad correspondiente y ejecuta una `tirada()`.
- Devuelve `True` si se produce un crítico, `False` en caso contrario.

### `esquivar(objetivo)`

Determina si el `objetivo` logra esquivar un ataque recibido.

- Funciona igual que `critico()`, pero evaluando la probabilidad de esquiva.

### `adicional(objetivo)`

Determina si el `objetivo` realiza un segundo ataque en el mismo turno.

- Se usa comúnmente tras realizar un `accion_basica()` para verificar si se repite el ataque.

---

## 🧩 Relación con otros módulos

El módulo `probabilidades.py` es utilizado directamente en:

- `jugador.py` y `enemigos.py`, durante las funciones `accion_basica()`, `ataque_adicional()` y cálculo de
  `calcular_golpe_recibido()`
- `efectos.py`, en `aplicar_efecto_contrario()` para verificar si un efecto logra aplicarse

Su diseño garantiza consistencia entre las clases y sus atributos probabilísticos, generando una experiencia de combate
variada y equilibrada.

---

## 🧠 Conclusión

El módulo `probabilidades.py` encapsula la lógica de azar en el combate, permitiendo controlar con claridad qué tan
probable es un efecto en función de la clase del personaje. Es sencillo, reutilizable y actúa como base para un sistema
de combate dinámico y estratégico.





