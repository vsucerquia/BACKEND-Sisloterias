# BACKEND-Sisloterias

Sistema de lotería con **API REST (FastAPI)**, **PostgreSQL en Neon** y **menú por consola** que consume la API solo por HTTP.

## Requisitos

- Python 3.10+
- Cuenta en [Neon](https://neon.tech) (cadena de conexión PostgreSQL)

## Configuración

1. Clona el repositorio y entra en la carpeta del backend.

2. Entorno virtual (recomendado):

   ```text
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala dependencias:

   ```text
   pip install -r requirements.txt
   ```

4. Crea el archivo **`.env`** en la raíz de este proyecto (junto a `app.py`). Puedes partir de **`.env.example`**:

   ```text
   copy .env.example .env
   ```

5. En Neon, copia la **connection string** de PostgreSQL y pégala en `.env`:

   ```env
   DATABASE_URL=postgresql://usuario:contraseña@ep-xxxxx.region.aws.neon.tech/neondb?sslmode=require
   ```

   Opcional para el menú cliente (por defecto es `http://127.0.0.1:8000`):

   ```env
   API_BASE_URL=http://127.0.0.1:8000
   ```

   No subas **`.env`** a Git (ya está en `.gitignore`).

## Crear tablas en la base de datos

Con la URL de Neon correcta en `.env`:

```text
python init_db.py
```

## Ejecutar la API (Uvicorn)

Desde la raíz del backend:

```text
python main.py
```

O:

```text
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Menú por consola (cliente HTTP)

En **otra terminal**, con la API ya en marcha:

```text
python menu_cli.py
```

El menú elige entidad y operaciones CRUD; todas las peticiones van a la API (no abre la base de datos directamente).

## Estructura del proyecto

```text
BACKEND-Sisloterias/
├── app.py                 # FastAPI + routers
├── main.py                # Arranque Uvicorn
├── menu_cli.py            # Menú consola → HTTP
├── init_db.py             # Crear tablas (ORM)
├── database/              # Motor y sesión SQLAlchemy
├── entities/              # Modelos ORM
├── schemas/               # Pydantic
├── endpoints/             # Routers por recurso
├── crud/                  # Cliente HTTP (CrudClient)
├── core/
└── utils/
```

## Entidades (6)

| Recurso   | Prefijo API   |
|----------|---------------|
| Jugador  | `/jugadores`  |
| Juego    | `/juegos`     |
| Sorteo   | `/sorteos`    |
| Boleto   | `/boletos`    |
| Premio   | `/premios`    |
| Pago     | `/pagos`      |

Cada uno expone: `GET /`, `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}`.

## Autor

Proyecto para el curso **Aplicación y Servicios Web**.

Autoras: Valeria y Valentina Sucerquia Álvarez.
