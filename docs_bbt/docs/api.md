# 🌐 API y Sistema de Ranking

Esta sección documenta en profundidad la **API REST** del proyecto y su integración con el **sistema de ranking**
mostrado en el frontend. Esta API permite acceder a los datos de los jugadores y visualizar un ranking dinámico ordenado
por diferentes criterios como nivel, victorias, derrotas u oro.

---

## 🧩 Estructura general de la API

La API está construida usando **Django REST Framework** y expone un punto principal: `/api/jugadores/`, correspondiente
al modelo `Jugador`.

### 🔗 URLs registradas (`urls.py`)

- `/api/jugadores/` → gestionado por `JugadorViewSet`
- `/api/` → raíz de la API, gestionado por `ApiRootViewSet`

Estas rutas se registran mediante un `DefaultRouter` de DRF, lo que permite exponer automáticamente las rutas estándar
de un `ModelViewSet`.

---

## 📦 Serializadores (`serializers.py`)

Se definen serializadores para varios modelos (`Jugador`, `Enemigo`, `Jefe`, `Combate`) pero el único que se utiliza en
esta API es:

- `JugadorSerializer`: serializa todos los campos del modelo `Jugador` usando `fields = '__all__'`.

Esto permite acceder de forma detallada a todos los atributos del jugador, aunque en la vista se formatea la salida
manualmente.

---

## 🔄 `JugadorViewSet`

### Tipo: `ModelViewSet`

### Permisos: `IsAuthenticated` (requiere autenticación)

### Filtros:

- Ordenamiento (`filters.OrderingFilter`)
- Campos disponibles: `id`, `nombre`, `victorias`, `derrotas`, `oro`, `nivel`
- Orden por defecto: `victorias` descendente

### Paginación: `CursorPagination` (recomendado para listas largas)

### Método personalizado: `list()`

En lugar de usar el comportamiento por defecto de DRF, se personaliza la respuesta para estructurar los datos de los
jugadores de forma específica. Cada jugador devuelto tiene esta estructura:

- `id_jugador`
- `usuario`: nombre de usuario de Django
- `nombre_personaje`
- `alineacion`
- `oro`
- `estadisticas`: diccionario con clase, nivel, experiencia, salud, energía, ataque, defensa, velocidad
- `victorias`
- `derrotas`
- `porcentaje_victorias`: calculado dinámicamente

Este método se adapta tanto si se usa paginación como si no.

---

## 🔍 `ApiRootViewSet`

Devuelve un diccionario con enlaces a los recursos disponibles. En este caso, solo expone el endpoint `jugadores`.

---

## 🧑‍💻 Integración con el Frontend (ranking)

El ranking se muestra en la página `ranking.html`. Este utiliza un archivo JS (`llamada_api.js`) que accede a la API
para cargar dinámicamente el top 5 de jugadores según el criterio elegido.

### 🖼️ Plantilla `ranking.html`

- Usa una estructura CSS para mostrar tarjetas de jugadores llamativa al usuario.
- Contiene filtros visuales para alternar entre ordenamiento por:
    - Nivel
    - Victorias
    - Derrotas
    - Oro
- Cada vez que se pulsa un botón, se llama a la función `cargarRanking()` con el criterio correspondiente.

---

## 📜 Script: `llamada_api.js`

Este script realiza una **petición asíncrona** a la API con ordenamiento dinámico según el botón pulsado. Por ejemplo:

- `/api/jugadores/?ordering=-nivel`
- `/api/jugadores/?ordering=-victorias`

### Flujo:

1. Se obtiene el `JSON` de respuesta de la API.
2. Se recorre el top 5 jugadores (`data.results` o `data.slice`).
3. Se genera el HTML para cada uno:
    - Imagen del personaje según su clase.
    - Nombre del personaje y usuario.
    - Dato destacado según el filtro activo.
    - Porcentaje de victorias si se muestra por victorias.

Esta lógica convierte la API en un recurso **interactivo y visual**, lo que mejora la experiencia de usuario y evita
recargar toda la página al cambiar de filtro.

---

## 📈 Escalabilidad

El sistema de ranking está preparado para escalar gracias a:

- Uso de paginación (`CursorPagination`)
- Serialización parcial y adaptada a cliente
- Consultas optimizadas por ordenamiento en la base de datos
- Facilidad de integración con asincronía (JavaScript dinámico)

---

## 📌 Consideraciones finales

Este módulo representa uno de los puntos fuertes del proyecto, ya que combina:

- Backend con Django REST Framework
- API autenticada y protegida
- Respuesta enriquecida con datos derivados (como el porcentaje de victorias)
- Frontend con actualización en tiempo real del ranking

Además, esta estructura puede reutilizarse fácilmente para exponer otras entidades del juego, como enemigos, combates o
estadísticas globales, con solo añadir nuevos `ViewSets` y `Serializers`.
