# 🚀 Despliegue del Proyecto

Battlebound Tactics ha sido diseñado para poder desplegarse fácilmente tanto en un entorno de desarrollo local como en
un servidor en la nube (AWS), utilizando **Docker** como sistema de contenedores. A continuación, detallo el proceso
completo de despliegue en ambas modalidades, así como los archivos utilizados para lograrlo.

---

## 🐳 Contenedorización con Docker

Todo el proyecto se ha encapsulado en un entorno Docker, asegurando consistencia entre entornos de desarrollo y
producción. Esto incluye:

- El backend con Django y sus dependencias.
- La base de datos **PostgreSQL**, tanto en local como en producción.
- Configuración de variables de entorno (gestionadas por archivos `.env`).
- Automatización del despliegue mediante **GitHub Actions**.

---

## 📁 Archivos de despliegue

| Archivo             | Descripción                                                                                          |
|---------------------|------------------------------------------------------------------------------------------------------|
| `Dockerfile`        | Define la imagen base del proyecto. Instala dependencias, copia el código y lanza el servidor.       |
| `compose.yml`       | Archivo principal para el despliegue en **AWS**. Usa PostgreSQL y está optimizado para producción.   |
| `compose_local.yml` | Versión adaptada para entorno de desarrollo local.                                                   |
| `docker_aws.yml`    | Workflow de **GitHub Actions** que automatiza la construcción, subida de imagen y despliegue en AWS. |

---

## 🏗️ Dockerfile: Imagen base del proyecto

Este archivo construye la imagen principal de Battlebound Tactics.

### Pasos que realiza:

- Utiliza una imagen oficial de Python como base.
- Instala las dependencias del proyecto desde `requirements.txt`.
- Copia todo el código del proyecto dentro del contenedor.
- Expone el puerto 8000.
- Ejecuta el servidor de Django en el puerto `0.0.0.0:8000`.

# Comando final de ejecución:

python manage.py runserver 0.0.0.0:8000

---

## 💻 Despliegue local: `compose_local.yml`

Este archivo se usa para desarrollo en entorno local.

### Características:

- Define un servicio `web` que ejecuta la aplicación Django.
- Expone el puerto 8000 en el host.
- Usa volúmenes para mantener sincronizado el código entre el host y el contenedor.
- Conecta con un contenedor de base de datos PostgreSQL también definido en el archivo.

# Comando para ejecutarlo:

docker compose -f compose_local.yml up --build

---

## ☁️ Despliegue en producción: `compose.yml`

Este archivo es el utilizado para el **despliegue real en AWS**. Está adaptado para correr la aplicación en un servidor
EC2 con Docker.

### Características:

- Lanza dos servicios principales: `app` (Battlebound Tactics) y `db` (PostgreSQL).
- Usa traefik como reverse-proxy.
- Conecta a una base de datos PostgreSQL real y persistente.
- Exposición de puertos y variables de entorno según la configuración definida en `.env`.

# Comando de despliegue en AWS:

docker compose up -d

---

## 🤖 Despliegue automatizado: `docker_aws.yml` (GitHub Actions)

Este archivo no es parte del despliegue manual, sino una automatización que se ejecuta al hacer **push** o **pull
request** en el repositorio de GitHub.

### Funcionalidad:

- Se activa en eventos del repositorio.
- Construye una nueva imagen Docker a partir del código actualizado.
- Sube la imagen actualizada a Docker Hub.
- Se conecta por SSH a la instancia EC2 de AWS.
- Detiene cualquier contenedor anterior y lanza uno nuevo con la imagen actualizada.

Gracias a este sistema, no es necesario acceder manualmente al servidor para desplegar una nueva versión: basta con
hacer push al repositorio.

---

## 📦 Resultado

Al completar el proceso de despliegue, el proyecto queda corriendo en un contenedor Docker en AWS, utilizando PostgreSQL
como base de datos y estando completamente accesible desde su dominio vinculado ([`jonatan-daw2.tech`](https://jonatan-daw2.tech/)). Además, con la
automatización configurada, cualquier cambio en el repositorio se refleja automáticamente tras cada push.
