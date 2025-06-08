# 🌐 Vistas de Django

Esta sección documenta en detalle cada una de las vistas del proyecto, mostrando los parámetros recibidos y
decoradores aplicados. Aquí explico cómo cada vista contribuye a la funcionalidad del juego.

---

## 🖼️ BienvenidaPageView(request)

**Decoradores**: Ninguno  
**Parámetros**: `request`

Vista de tipo `TemplateView` que carga la plantilla de bienvenida. Es la pantalla inicial que ve el usuario antes de
iniciar sesión o registrarse. No requiere autenticación.

---

## 🏠 InicioPageView(request)

**Decoradores**: `LoginRequiredMixin`  
**Parámetros**: `request`

Esta vista principal se muestra tras iniciar sesión. Calcula el porcentaje de salud, energía y experiencia del jugador
para mostrarlos gráficamente. También muestra las rutas disponibles: mapa, fuente, equipo, habilidades y ranking.

---

## 🗺️ MapaContinentePageView(request)

**Decoradores**: `LoginRequiredMixin`  
**Parámetros**: `request`

Muestra el mapa general del continente. Es una plantilla estática que permite al jugador seleccionar una región
específica para explorar.

---

## 🌍 RegionPageView(request)

**Decoradores**: `LoginRequiredMixin`  
**Parámetros**: `request`

Muestra una región concreta con enemigos aleatorios. Excluye jefes (salvo uno especial que sí puede aparecer en una
ubicación preseleccionada) y muestra siete enemigos diferentes. Cada zona del mapa puede presentar un enemigo distinto.

---

## 👤 RegistroPageView(request)

**Decoradores**: Ninguno  
**Parámetros**: `request`

Vista basada en formularios (`FormView`) que gestiona el registro del usuario. Crea un usuario en base al modelo
`Jugador`, le asigna una pasiva aleatoria y luego inicia sesión automáticamente con `login`.

---

## 🔐 LoginUserView(request)

**Decoradores**: Ninguno  
**Parámetros**: `request`

Vista heredada de `LoginView` de Django. Muestra el formulario de login de usuarios, cuenta con una plantilla
personalizada.

---

## 🏆 RankingPageView(request)

**Decoradores**: `LoginRequiredMixin`  
**Parámetros**: `request`

Muestra el ranking general de jugadores. Aquí mostramos los 5 mejores jugadores ordenados por categorías (oro,
victorias, derrotas y nivel), esto lo hacemos mediante el uso de una API propia que contiene esta información.

---

## 🏰 CastlevyrPageView(request)

**Decoradores**: `LoginRequiredMixin`  
**Parámetros**: `request`

Vista que representa el castillo final del juego. Carga un jefe específico llamado "Havva Skript" y prepara al jugador
para enfrentarlo. Esta vista representa el punto culminante de la versión actual del juego.

---

## ⚔️ equipamiento(request)

**Decoradores**: `@login_required`  
**Parámetros**: `request`

Permite al jugador cambiar su arma o accesorio. Verifica que el jugador tenga el nivel necesario antes de aplicar los
cambios. Carga todos los objetos disponibles y actualiza a nuestro jugador.

---

## 📚 habilidades(request)

**Decoradores**: `@login_required`  
**Parámetros**: `request`

Permite al jugador gestionar sus habilidades. Valida si cuenta con el nivel necesario para equiparlas y permite
sustituir cualquiera de las tres ranuras disponibles. Usa el modelo `Activa`.

---

## ⚔️ iniciar_combate(request, enemigo_id)

**Decoradores**: `@login_required`, `@require_GET`  
**Parámetros**: `request`, `enemigo_id`

Inicializa un nuevo combate contra el enemigo seleccionado. Crea una instancia del modelo `Combate`, guardando el
jugador y el enemigo involucrados, y redirige a la vista `combate`.

---

## 🧠 combate(request, combate_id)

**Decoradores**: `@login_required`  
**Parámetros**: `request`, `combate_id`

Vista central de combate por turnos. Controla la lógica del enfrentamiento:

- Aplica efectos de estado
- Determina el orden de turnos por velocidad
- Ejecuta acciones del jugador y del enemigo
- Registra logs y efectos visuales
- Actualiza el turno en el modelo `Combate`

Trabaja con múltiples módulos del núcleo (`estadisticas.py`, `jugador.py`, `enemigos.py`, `efectos.py`,
`utils_resolvedor.py`) y es la pieza más importante de la mecánica del juego.

Para más detalles, por favor, consulte nuestra [⚔️ Lógica del Combate](logica-combate.md)

---

## 🎯 resultado_combate(request, combate_id)

**Decoradores**: ninguno  
**Parámetros**: `request`, `combate_id`

Muestra el resultado final del combate: victoria o derrota. Carga todos los datos relevantes desde la instancia del
modelo `Combate` y los pasa a la plantilla `resultado.html`.

---

## 💧 fuente(request)

**Decoradores**: ninguno  
**Parámetros**: `request`

Restaura completamente la salud y energía del jugador, luego, redirige al `inicio`.

---

## 🛠️ Comentadas: abandonar_combate, verificar_abandono, resolver_abandono

**Decoradores**: (comentados)  
**Parámetros**: varios

Estas funciones están desactivadas actualmente, pero estaban diseñadas para registrar el abandono de un combate.
Incluyen opciones para continuar o rendirse, y estaban pensadas para prevenir exploits o fallos en el flujo de batalla.

---