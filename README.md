# API REST de Gestión de Películas

Esta es una API RESTful desarrollada con Flask y SQLAlchemy para gestionar un catálogo de películas. Permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre los registros y obtener estadísticas generales de la colección de manera sencilla.

---

## Tecnologías Utilizadas

* Python 3
* Flask
* Flask-SQLAlchemy
* SQLite (Base de datos por defecto)

---

## Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

1. Clona este repositorio o descarga el código fuente en tu computadora.
2. Crea un entorno virtual (recomendado) ejecutando `python -m venv env` en tu terminal.
3. Activa el entorno virtual (usa `env\Scripts\activate` en Windows o `source env/bin/activate` en macOS/Linux).
4. Instala las dependencias necesarias ejecutando `pip install Flask Flask-SQLAlchemy`.
5. Inicia el servidor ejecutando `python nombre_de_tu_archivo.py`.

El servidor estará disponible en `http://localhost:5000`. La base de datos `peliculas.db` se creará automáticamente la primera vez que inicies la aplicación.

---

## Referencia de la API (Endpoints)

| Método | Ruta | Descripción |
|---|---|---|
| **GET** | `/` | Mensaje de bienvenida y estado de la API. |
| **GET** | `/peliculas` | Obtiene todas las películas. Soporta filtros `?genero=X` y `?orden=calificacion`. |
| **GET** | `/peliculas/<id>` | Obtiene los detalles de una película específica por su ID. |
| **POST** | `/peliculas` | Crea un nuevo registro de película. |
| **PUT** | `/peliculas/<id>` | Modifica los datos de una película existente. |
| **DELETE**| `/peliculas/<id>` | Elimina una película de la base de datos. |
| **GET** | `/peliculas/estadisticas/resumen` | Muestra métricas (total, promedio de calificación, mejor y peor película). |

---

## Ejemplos de Uso

### Crear una película nueva (POST `/peliculas`)

Debes enviar un cuerpo en formato JSON con los datos de la película. Los campos `titulo`, `genero` y `calificacion` son obligatorios.

**Cuerpo de la petición (JSON):**
```json
{
    "titulo": "Inception",
    "genero": "Ciencia Ficción",
    "calificacion": 8.8,
    "director": "Christopher Nolan",
    "anio": 2010,
    "duracion": 148
}
