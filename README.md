# PROYECTO INTEGRADO

## Battlebound Tactics

![Portada del proyecto](static/resources/portada.png)

| Autor: *Jonatan García Luna*           |
|----------------------------------------|
| Tutor: **Jose Luis de Diego González** |

| I.E.S. Francisco Romero Vargas (Jerez de la Frontera) |
|-------------------------------------------------------|
| Desarrollo de Aplicaciones Web                        |
| Curso: 2024/2025                                      |

---

## Tabla de contenido

- [Diseño y Planificación del Proyecto](#diseño-y-planificación-del-proyecto)
    - [Introducción](#introducción)
    - [Finalidad](#finalidad)
    - [Objetivos](#objetivos)
    - [Medios necesarios](#medios-necesarios)
    - [Planificación](#planificación)
- [Realización del Proyecto](#realización-del-proyecto)
    - [Desarrollo técnico](#desarrollo-técnico)
    - [Sistema de combate y módulos principales](#sistema-de-combate-y-módulos-principales)
    - [Estructura de vistas de Django](#estructura-de-vistas-de-django)
    - [Trabajos realizados](#trabajos-realizados)
    - [Problemas encontrados](#problemas-encontrados)
    - [Modificaciones sobre el proyecto planteado inicialmente](#modificaciones-sobre-el-proyecto-planteado-inicialmente)
    - [Posibles mejoras al proyecto](#posibles-mejoras-al-proyecto)
    - [Bibliografía](#bibliografía)

---

## Diseño y Planificación del Proyecto

### Introducción

Battlebound Tactics es una aplicación web que presenta un videojuego de combate por turnos con mecánicas inspiradas en
los RPG clásicos. El jugador creará su personaje, subirá de nivel, aprenderá habilidades, equipará armas y se enfrentará
a enemigos únicos con IA propia. A través de un mapa interactivo, el jugador podrá explorar distintas regiones,
enfrentarse a jefes y progresar en un mundo que evoluciona.

### Finalidad

Permitir a los usuarios disfrutar de un juego completo estilo RPG con un sistema de combate profundo, donde puedan tomar
decisiones tácticas, personalizar sus builds y enfrentarse a desafíos crecientes en un entorno web accesible.

### Objetivos

- Desarrollar un sistema de combate táctico por turnos con lógica avanzada.
- Integrar habilidades únicas con efectos diversos (curación, daño, buffs/debuffs, veneno, etc.).
- Crear un sistema de IA enemiga que actúe de forma estratégica según la situación.
- Permitir la evolución del personaje mediante niveles, equipo y habilidades.
- Diseñar una interfaz visual atractiva y funcional.
- Incorporar funcionalidades como ranking, mapa interactivo, inventario y fuente de curación.
- Implementar registro y autenticación de usuarios.
- Integrar una API para el ranking de los jugadores.

---

## Medios necesarios

### Hardware:

- Ordenador principal: Ryzen9 7900X3D, 32GB RAM DDR5
- Portátil secundario: Ryzen5 5700U, 16GB RAM DDR5

### Software:

- **Lenguajes de programación:** HTML, CSS, JavaScript, Python.
- **Frameworks y librerías:** Django, Bootstrap 5.
- **Para el despliegue:** Docker, Dockerhub y servicios de AWS (Instancias de EC2), servicios de .Tech Domains.
- **Otros:** Pillow, Sora AI (para imágenes)

### Herramientas:

- Visual Studio Code
- PyCharm
- Mozilla Firefox, Google Chrome
- Oracle VirtualBox

---

## Planificación

#### 1. **Definición inicial (1–1.5 semanas)**

- **Diseño conceptual del juego**: se establecieron las mecánicas principales (combate por turnos, progresión por
  niveles,
  habilidades y equipo).
- **Diseño de base de datos**: definición de modelos con el ORM de Django, incluyendo:
    - `Jugador`: estadísticas, experiencia, clase, pasiva.
    - `Enemigo`: nombre, tipo, dificultad, habilidades disponibles.
    - `Activa`,`ActivaEnemigo`, `Arma`, `Accesorio`, `Pasiva`, `Combate`.
- **Estructura del proyecto Django**: creación del entorno virtual, configuración de `settings.py`, estructura de apps y
  rutas base.
- **Primeros bocetos**: ideas visuales de cómo debía lucir el mapa, el personaje y el combate.
- **Preparación del sistema de autenticación**: integración de los formularios de registro y login básicos.

#### 2. **Desarrollo de lógica de combate (2.5–3 semanas)**

- **Construcción de los módulos en `core/`**:
    - `jugador.py`: ataques, habilidades, defensa, evasión, regeneración de energía y salud.
    - `enemigos.py`: lógica de IA para selección de acciones, cálculos y cooldowns.
    - `efectos.py`: aplicación y duración de efectos positivos y negativos.
    - `estadisticas.py`: cálculo de estadísticas durante el combate.
    - `utils_resolvedor.py`: resolución del turno, condiciones de victoria y derrota.
- **Turnos por velocidad**: prioridad basada en la estadística de velocidad.
- **Combate paso a paso**: integración del sistema por turnos con lógica condicional (curarse, atacar, aplicar veneno,
  etc.).
- **Sistema de experiencia y subida de nivel**: experiencia ganada al finalizar un combate, aumento de estadísticas
  automáticamente.
- **Pasivas únicas**: al registrarse, cada jugador obtiene una pasiva distinta con bonus únicos.
- **Balance de clases y enemigos**: ajuste de estadísticas para que haya diferencias reales entre builds ofensivas y
  defensivas.

#### 3. **Diseño del frontend (2 semanas)**

- **Plantillas HTML**: diseño de las vistas principales (`inicio`, `mapa`, `combate`, `ranking`, `equipo`,
  `habilidades`, `fuente`).
- **Sistema de estadísticas visual**: barra de vida, energía y experiencia representadas gráficamente.
- **Mapa interactivo**: con botones para acceder a regiones y encuentros aleatorios o jefes.
- **Menús dinámicos**: navegación rápida por el juego con transiciones suaves.
- **Animaciones y estilos CSS**: efectos visuales durante combate y pantallas de victoria/derrota.
- **Verificación visual de requisitos**: deshabilitación de botones si el jugador no cumple los requisitos de nivel para
  usar armas o habilidades.
- **Diferentes estados visuales del personaje**: imágenes personalizadas según ubicación (inicio, combate, resultados,
  ranking).

#### 4. **Pruebas e integración (1 semana)**

- **Pruebas del sistema de combate**:
    - Verificación de daño, efectos, turnos, regeneración.
    - Casos especiales.
- **Simulación de comportamiento de IA**: comprobar que el enemigo actúa de forma coherente (atacar si el jugador está
  débil, curarse si tiene poca vida, etc.).
- **Depuración de errores**: ajustes de funciones que provocaban comportamiento inesperado (por ejemplo, errores en
  cálculo de daño al aplicar curaciones).
- **Tests de frontend**: comprobación de renderizado correcto en navegadores, validación de formularios, rutas
  protegidas.
- **Equilibrado del juego**: modificaciones de valores base (daño, coste de energía, duración de efectos) tras pruebas
  reales.
- **Comprobación de experiencia de usuario completa**: flujo completo desde login → mapa → combate → victoria → subir
  nivel → volver al mapa.

#### 5. **Despliegue y documentación (1 semana)**

- **Contenedorización con Docker**:
    - `Dockerfile` para construir imagen de Django.
    - `compose.yml` con configuración completa del entorno.
- **Archivo `requirements.txt`** actualizado con todas las dependencias.
- **Ignorados (`.gitignore`, `.dockerignore`)**: limpieza del repositorio y el contenedor de archivos innecesarios.
- **Pruebas en entorno real (EC2)**: ejecución del juego en AWS EC2, verificación de funcionamiento y rendimiento.
- **Redacción de README**:
- **Comentarios en el código fuente**: documentación interna en las funciones más relevantes del sistema de combate.

---

## Realización del Proyecto

### Desarrollo técnico

La aplicación fue diseñada con Django, combinando lógica de juego en el backend con una interfaz visual interactiva en
el frontend. Todo el sistema está dividido en módulos para facilitar el mantenimiento y la escalabilidad futura.

### Sistema de combate y módulos principales

Los archivos principales del directorio `core/` son:

#### 🛡️ `combate/jugador.py`

- Ejecuta acciones del jugador: ataques, habilidades, defensa, evasión.
- Calcula daño infligido y energía usada.
- Gestiona experiencia y niveles.

#### 🧠 `combate/enemigos.py`

- Controla la IA del enemigo.
- Escoge habilidades según estado del combate.
- Gestiona cooldowns y condiciones.

#### ☠️ `combate/efectos.py`

- Aplica efectos de estado: veneno, buff, debuff.
- Controla su duración y efecto en combate.
- Permite renovación o extensión según el caso.

#### 📊 `globales/estadisticas.py`

- Calcula estadísticas finales combinando nivel, pasiva y equipo.
- Determina velocidad, daño, evasión y otros modificadores.

#### 🎲 `globales/probabilidades.py`

- Define probabilidades por clase: críticos, evasión, ataques dobles.
- Centraliza la lógica de tiradas aleatorias.

#### 🧩 `combate/utils_combate.py`

- Lee datos de habilidades.
- Interpreta y organiza efectos de forma estándar.

#### 🚦 `combate/utils_resolvedor.py`

- Inicia el combate.
- Aplica efectos de estado al iniciar el turno.
- Verifica condiciones de victoria o derrota.

### Estructura de vistas de Django

Las vistas definen la interacción entre usuario y sistema. Algunas destacadas:

- **`inicio`**: pantalla principal con acceso al mapa y resto de funcionalidades.
- **`mapa`, `region`**: selección de enemigos y zonas del mundo.
- **`castlevyr`**: zona de jefe final.
- **`combate`**: alternancia de turnos, cálculo de acciones y renderizado del combate.
- **`iniciar_combate`**: prepara el estado inicial del combate.
- **`resultado_combate`**: muestra victoria o derrota.
- **`equipo`, `habilidades`**: permiten cambiar configuraciones de personaje.
- **`fuente`**: curación total del jugador.
- **`ranking`**: muestra a los mejores jugadores.
- **`registro`**: registro de usuario y creación del personaje con pasiva única.

### Desarrollo técnico

Lo primero que hice fue definir la estructura del proyecto en Django, estableciendo los modelos principales: Jugador,
Enemigo, Habilidad, Arma, Accesorio, Pasiva y Combate. Gracias al ORM de Django, pude trabajar de forma rápida y
ordenada, asegurando relaciones consistentes y un backend sólido.

Una vez definidos los modelos, me centré en el desarrollo de la lógica de combate. Esta fue, sin duda, la parte más
compleja y ambiciosa del proyecto. Implementé dos grandes módulos:

- **Lógica del Jugador (`jugador.py`)**: programé el comportamiento del jugador en combate, incluyendo ataques básicos,
  críticos, uso de habilidades con costes, recuperación de energía y salud y efectos aplicados.

- **Lógica del Enemigo (`enemigos.py`)**: desarrollé una IA capaz de elegir acciones según el
  estado del combate, gestionar cooldowns y aplicar daño, curaciones (a sí mismo) o estados al jugador.

Además, implementé un sistema de **estados y efectos (`efectos.py`)**, que permite aplicar buffs, debuffs y efectos
negativos como veneno o estados alterados, con duración limitada y comportamiento acumulativo. Estos efectos se aplican
al inicio de cada turno y son gestionados en tiempo real, permitiendo interacciones interesantes durante el combate.

Para centralizar las estadísticas, creé el archivo `estadisticas.py`, que calcula dinámicamente las estadísticas
completas de jugadores y enemigos teniendo en cuenta pasivas, equipo y otros modificadores. Este sistema asegura un
equilibrio coherente entre los personajes.

Además, incluí útiles que ayudan en el manejo del combate, como `utils_combate.py`, `utils_resolvedor.py`
y `probabilidades.py`, cada uno con funciones auxiliares para leer efectos, calcular probabilidades o controlar el flujo
de la partida.

En `views.py` integré toda la lógica del backend con el frontend. Aquí se encuentra el control de los turnos de combate,
la inicialización del mismo, la alternancia entre jugador y enemigo, y el renderizado del estado actual con los logs de
acción. La vista de combate fue clave para conectar el motor de juego con la experiencia visual.

También desarrollé un conjunto de pantallas accesibles desde el menú principal: mapa del mundo, fuente de curación,
inventario, habilidades y ranking. Todo esto se diseñó con las templates de Django, CSS y JavaScript, cuidando la
presentación para que el usuario tuviera una experiencia agradable y envolvente.

### Ficheros y configuración

Para el despliegue, preparé el proyecto con `Docker`, incluyendo un `Dockerfile` y un `compose.yml`. También creé un
`requirements.txt` con todas las dependencias necesarias.

### Documentación y pruebas

Documenté cuidadosamente cada función y módulo del proyecto, especialmente en las partes más sensibles como el combate y
el tratamiento de efectos. También realicé muchas pruebas manuales durante los turnos de combate, asegurándome de que el
flujo fuera correcto, que los efectos se aplicaran adecuadamente, y que la IA del enemigo reaccionara con lógica a
diferentes situaciones.

### Conclusión

A lo largo de este proceso, he aprendido a estructurar y mantener un proyecto web complejo, a implementar lógica de
juego desde cero, y a combinar correctamente backend y frontend. También he entendido la importancia de una buena
documentación, tanto a nivel de código como de usuario. El resultado es un proyecto funcional, divertido y abierto a
futuras ampliaciones.

### Trabajos realizados

A lo largo del desarrollo de este proyecto he realizado múltiples tareas que abarcan tanto el diseño como la
implementación de funcionalidades complejas al sistema. Todo el trabajo se ha dividido en fases con objetivos
específicos y bien definidos. A continuación, detallo los trabajos más relevantes que he llevado a cabo:

- **Definición del concepto de juego**: concebí un videojuego de combate por turnos con elementos RPG, enfocado en la
  estrategia, la gestión de recursos (salud, energía, estados) y la progresión del personaje.

- **Diseño de la estructura del proyecto en Django**: configuré el entorno de trabajo, creé la estructura base del
  proyecto y definí todos los modelos necesarios para representar las entidades del juego (jugador, enemigos,
  habilidades, equipo, combate, etc.).

- **Implementación de la lógica de combate**: desarrollé desde cero todo el sistema de combate por turnos, tanto para el
  jugador como para los enemigos, incluyendo:
    - Ataques básicos, críticos y adicionales.
    - Habilidades con efectos variados y únicos.
    - Aplicación de estados con duración, acumulación y expiración.
    - Turnos alternos basados en velocidad.
    - IA enemiga que elige sus acciones estratégicamente.

- **Gestión avanzada de estadísticas**: programé funciones para calcular las estadísticas completas de cada entidad
  teniendo en cuenta pasivas, armas, accesorios y su nivel, permitiendo una progresión personalizada y equilibrada.

- **Desarrollo del frontend con las templates de Django**: creé las interfaces principales del juego (inicio, combate,
  mapa,
  habilidades, equipo, fuente sagrada, ranking...) con HTML, CSS y JavaScript, conectadas dinámicamente al backend.

- **Pruebas funcionales y ajuste de balance**: realicé pruebas manuales completas del sistema de combate y de toda la
  experiencia de usuario, ajustando valores y corrigiendo errores según era necesario, aunque según vaya avanzando la
  aplicación me gustaría seguir haciendo cambios de balance periódicos.

- **Documentación y preparación del despliegue**: redacté la documentación del proyecto, configuré el despliegue
  mediante Docker y dejé preparado el repositorio en GitHub con toda la información pertinente.

En resumen, he trabajado en todos los aspectos del desarrollo del proyecto, desde el diseño inicial hasta la
programación, las pruebas, la documentación y la publicación final. Todo el trabajo ha sido hecho desde cero y
cuidadosamente estructurado para que el juego sea funcional, comprensible y mantenible.

### Problemas encontrados

- A la hora de desarrollar el backend no he tenido muchos problemas, sabía lo que hacía y lo que quería, no ha
  presentado graves problemas salvo alguno que otro con las funciones más complejas, pero he logrado solucionarlas
  rápidamente
- A la hora de desarrollar el frontend sí que me ha sido un poco más complicado, JavaScript me ha causado más de un
  quebradero de cabeza, pero siempre he encontrado la manera de poder salir del atasco y obtener un resultado
  satisfactorio. Con CSS también he tenido problemas, pero no por falta de habilidades, yo quería un diseño muy único y
  específico y ha requerido muchísimo trabajo, por ejemplo, ajustar correctamente los mapas correctamentes fue bastante
  complicado
- A la hora de desplegar la aplicación me he encontrado con varios problemas de compatibilidad, principalmente porque la
  aplicación era muy grande para la capa gratuita de AWS, me he visto obligado a reducir (e incluso quitar) varias
  funcionalidades de la aplicación como, por ejemplo, el sistema de música

### Modificaciones sobre el proyecto planteado inicialmente

- No he podido desarrollar el sistema de tiendas ni el sistema de combates entre jugadores por falta de tiempo y de
  ideas, también he tenido que recortar algunas otras funciones por el mismo motivo. He pensado que para añadir algo mal
  y rápido prefiero no hacerlo de momento y añadirlo en un futuro, la lista de modificaciones que he hecho son:
    - Borrar el sistema de tiendas (falta de tiempo)
    - Borrar el sistema de objetos y mochilas (falta de ideas, podría colisionar con mi idea de habilidades)
    - Borrar el Hidden Potential (sistema para mejorar personajes, descartado por el sistema de ahora de subir de nivel)
    - Borrar el sistema de combates entre jugadores (falta de ideas, sería lo mismo que un combate normal pero en vez de
      luchar contra un enemigo lo harías contra un jugador)

### Posibles mejoras al proyecto

- Añadir el sistema de tiendas, hacer que rote cada 24 horas con Celery (extensión de Python)
- Añadir el combate entre jugadores
- Añadir un sistema que verifique el abandono de combates
- Añadir los objetos con un enfoque distinto
- Añadir combates de dos o más jugadores contra un super enemigo
- Profundizar más en el concepto de los jefes, hacer que tengan batallas con mecánicas únicas
- Terminar el resto de reinos

### Bibliografía

Durante el desarrollo de este proyecto he consultado diversas fuentes que me han servido de apoyo tanto para resolver
dudas técnicas como para tomar decisiones de diseño. A continuación, listo las más relevantes:

### Bibliografía

- [Django Documentation](https://docs.djangoproject.com)
- [Python Docs](https://docs.python.org/3/)
- [MDN Web Docs](https://developer.mozilla.org)
- [W3Schools](https://www.w3schools.com/)
- [Stack Overflow](https://stackoverflow.com)
- Material aportado por los docentes del módulo DAW
- Sora AI (generación de imágenes para personajes y pantallas)

---

## A disfrutar de Battlebound Tactics!

![Goku aproves](static/resources/goku_thumbs_up.gif)
