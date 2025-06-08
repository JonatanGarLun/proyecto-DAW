# ✅ Conclusiones Finales

El desarrollo de **Battlebound Tactics** ha supuesto un proceso intenso, desafiante y muy gratificante, en el que he
abordado de forma integral el diseño, construcción, pruebas y despliegue de una aplicación web que combina los
principios de desarrollo backend con una experiencia visual frontend envolvente, todo ello dentro de un sistema de
combate táctico por turnos.

---

## 🔍 Visión General del Trabajo Realizado

Desde el inicio del proyecto, me propuse diseñar un juego web completo con mecánicas inspiradas en los RPG clásicos, que
ofreciera al jugador una experiencia estratégica, envolvente y entretenida. El proyecto ha abarcado:

- La definición de una base de datos compleja con modelos como `Jugador`, `Enemigo`, `Habilidad`, `Pasiva`, `Arma`,
  `Accesorio`, y `Combate`.
- La creación del sistema de combate por turnos más profundo que he desarrollado hasta la fecha, con IA enemiga,
  habilidades activas y pasivas, efectos de estado y estadísticas dinámicas.
- El diseño de una interfaz de usuario visualmente atractiva y coherente, basada en plantillas HTML, CSS personalizado y
  lógica de interacción con JavaScript.
- La integración de funcionalidades clave como: mapa interactivo, zonas de jefes, sistema de curación, ranking de
  jugadores a través de una API, gestión de equipo, habilidades, y registro/login personalizado con pasivas únicas.
- El uso de **Docker** para contenedorización y **GitHub Actions** para automatizar el despliegue en **AWS**,
  garantizando una entrega profesional del producto final.

---

## ⚠️ Principales Dificultades

Durante el desarrollo me enfrenté a múltiples retos técnicos:

- **Lógica compleja del combate**: La cantidad de condiciones, efectos, turnos y ramificaciones del sistema de combate
  requirió un diseño modular y cuidadoso. Resolver los efectos acumulativos, el flujo de los turnos, y la IA enemiga me
  exigió una gran precisión.

- **Frontend avanzado**: Aunque tenía más experiencia en backend, enfrentarme a interacciones complejas con JavaScript
  (como las animaciones del combate o las peticiones a la API) fue un desafío que logré superar con investigación y
  dedicación constantes.

- **Despliegue en AWS**: El entorno gratuito de AWS presentó límites de recursos que me obligaron a optimizar el
  proyecto, deshabilitando funciones no esenciales como la música de fondo para evitar saturar el servidor.

- **Diseño visual personalizado**: Me propuse un diseño muy específico para los mapas y pantallas, lo que implicó muchas
  horas ajustando estilos CSS y capas visuales para que el resultado final fuese fiel a la idea original que tenía
  en mente.

---

## 📈 Evolución del Proyecto

Si bien la planificación inicial era ambiciosa, durante el desarrollo fue necesario realizar ajustes realistas. Algunas
funcionalidades como el sistema de tiendas, combates PvP o inventario de objetos fueron finalmente descartadas, no por
falta de capacidad, sino por una decisión de priorizar **calidad sobre cantidad**. Prefiero no incluir una funcionalidad
que no está madura, que implementarla de forma incompleta o apresurada.

Estos ajustes me permitieron centrarme en lo verdaderamente importante: un sistema de combate sólido, una experiencia
jugable clara, y una interfaz pulida. Cada modificación que se hizo al plan inicial fue razonada, documentada y
ejecutada con criterio.

---

## ✅ Estado Final del Proyecto

Actualmente, *Battlebound Tactics* incluye:

- Sistema completo de combate por turnos, con IA enemiga, efectos de estado, pasivas y habilidades.
- Progresión del jugador basada en experiencia, niveles, equipo y estadísticas calculadas dinámicamente durante el
  combate.
- Múltiples pantallas accesibles desde un menú visual: mapa del mundo, combate, jefe final (castillo), equipo,
  habilidades, fuente, y ranking.
- Sistema de autenticación con registro personalizado que asigna una pasiva aleatoria.
- API REST funcional para acceder al top de jugadores, consumida por la vista de ranking.
- Despliegue contenedorizado con Docker y actualización automática mediante GitHub Actions.

El juego funciona correctamente, tiene flujo completo desde el login hasta la pantalla de victoria, y se encuentra
**preparado para futuras ampliaciones**.

---

## 📚 Aprendizajes y Valoración

Este proyecto ha sido un verdadero viaje de crecimiento personal y profesional. He aprendido:

- A **modularizar** correctamente la lógica compleja.
- A integrar frontend y backend de forma fluida.
- A desplegar con herramientas modernas como Docker y GitHub Actions.
- A **documentar** cada componente del proyecto, desde el diseño conceptual hasta la API y el despliegue.
- A **resolver problemas reales** en tiempo real, haciendo pruebas y ajustes en cada fase del desarrollo.

Además, este trabajo me ha enseñado a tomar decisiones de diseño, priorizar tareas y construir una aplicación que no
solo sea funcional, sino también mantenible, escalable y atractiva visualmente.

---

## 🎉 Cierre

Battlebound Tactics no es solo un juego: es la culminación de todo lo aprendido durante mi formación. Estoy orgulloso
del resultado y de haber podido entregar un producto completo, divertido y técnicamente sólido. Todo el trabajo —desde
el código hasta la documentación— ha sido hecho desde cero y con máxima dedicación y cariño.

Muchas gracias por acompañarme hasta el final de este viaje.

**— Jonatan García Luna**

![Portada del proyecto](../../static/resources/goku-final.gif)