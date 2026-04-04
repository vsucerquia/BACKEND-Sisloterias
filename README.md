# BACKEND-Sisloterias
Sistema de Lotería desarrollado para simular el funcionamiento básico de un sorteo, permitiendo la generación de números aleatorios, registro de jugadores y validación de ganadores.

# Sistema de Lotería / Apuestas – API REST con FastAPI

## Descripción

Este proyecto implementa una **API REST utilizando FastAPI** para gestionar un sistema de **lotería y apuestas**.

La aplicación permite realizar operaciones **CRUD (Crear, Leer, Actualizar, Eliminar)** sobre las diferentes entidades del sistema mediante endpoints HTTP.

El proyecto utiliza:

* **FastAPI** para la API
* **PostgreSQL (Neon)** como base de datos
* **SQLAlchemy** como ORM
* **Pydantic** para validación de datos
* **Uvicorn** como servidor ASGI
* **Requests / HTTPX** para el cliente HTTP del menú por consola

Además incluye un **menú por consola que consume la API mediante peticiones HTTP**.

---

# Tecnologías utilizadas

* Python 3.10+
* FastAPI
* Uvicorn
* PostgreSQL (Neon)
* SQLAlchemy
* Pydantic
* Requests / HTTPX
* python-dotenv
* bcrypt

---

# Arquitectura del proyecto

El proyecto sigue una **arquitectura modular** separando responsabilidades por capas.

```
src/
│
├── app.py                       # Aplicación FastAPI y registro de routers
│
├── core/                        # Núcleo del sistema
│   ├── exceptions.py
│   ├── responses.py
│   └── error_handlers.py
│
├── database/
│   └── database.py              # Conexión a PostgreSQL
│
├── entities/                    # Modelos ORM (SQLAlchemy)
│   ├── jugador.py
│   ├── juego.py
│   ├── sorteo.py
│   ├── boleto.py
│   ├── premio.py
│   └── pago.py
│
├── schemas/                     # Modelos Pydantic
│   ├── jugador_schema.py
│   ├── juego_schema.py
│   ├── sorteo_schema.py
│   ├── boleto_schema.py
│   ├── premio_schema.py
│   └── pago_schema.py
│
├── endpoints/                   # Rutas FastAPI
│   ├── jugadores_router.py
│   ├── juegos_router.py
│   ├── sorteos_router.py
│   ├── boletos_router.py
│   ├── premios_router.py
│   └── pagos_router.py
│
├── crud/                        # Cliente HTTP para consumir la API
│   └── crud_client.py
│
├── utils/
│   └── security.py
│
├── main.py                      # Menú por consola
├── init_db.py                   # Script para crear tablas
│
├── requirements.txt
└── README.md
```

---

# Entidades del sistema

El sistema incluye **6 entidades principales**:

### Jugador

Representa al usuario que participa en el sistema.

### Juego

Tipo de juego disponible (lotería, ruleta, bingo).

### Sorteo

Evento donde se determina el número ganador.

### Boleto

Apuesta realizada por un jugador.

### Premio

Premio asignado a un boleto ganador.

### Pago

Registro del pago de un premio.

---

# Relaciones entre entidades

* Un **jugador** puede tener muchos **boletos**
* Un **juego** puede tener muchos **sorteos**
* Un **sorteo** puede tener muchos **boletos**
* Un **boleto** puede generar un **premio**
* Un **premio** puede registrar un **pago**

---

# Instalación

## 1. Clonar el repositorio

```
git clone https://github.com/tu-usuario/api-loteria-fastapi.git
cd api-loteria-fastapi
```

---

## 2. Crear entorno virtual

```
python -m venv venv
```

Activar entorno virtual:

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

---

## 3. Instalar dependencias

```
pip install -r requirements.txt
```

---

# Configuración de base de datos

Crear un archivo `.env` en la raíz del proyecto.

```
DATABASE_URL=postgresql://usuario:password@host/database
```

La base de datos utilizada es **PostgreSQL en Neon**.

---

# Crear tablas en la base de datos

Ejecutar el script:

```
python src/init_db.py
```

Esto creará todas las tablas definidas en los modelos ORM.

---

# Ejecutar la API

```
uvicorn src.app:app --reload
```

La API estará disponible en:

```
http://127.0.0.1:8000
```

---

# Documentación automática

FastAPI genera documentación automática con Swagger.

```
http://127.0.0.1:8000/docs
```

---

# Endpoints principales

## Jugadores

```
GET /jugadores
GET /jugadores/{id}
POST /jugadores
PUT /jugadores/{id}
DELETE /jugadores/{id}
```

## Juegos

```
GET /juegos
POST /juegos
PUT /juegos/{id}
DELETE /juegos/{id}
```

## Sorteos

```
GET /sorteos
POST /sorteos
PUT /sorteos/{id}
DELETE /sorteos/{id}
```

## Boletos

