# BACKEND-Sisloterias

Sistema de lotería con **API REST (FastAPI)**, **PostgreSQL en Neon** y **menú por consola** que consume la API solo por HTTP.

## Requisitos

- Python 3.10+
- Cuenta en Neon/PostgreSQL para obtener la cadena de conexión `DATABASE_URL`.

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

   También define **`SECRET_KEY`** (JWT, mínimo ~32 caracteres en producción), **`CORS_ORIGINS`**, y opcionalmente **`SEED_ADMIN_USER`** / **`SEED_ADMIN_PASSWORD`** (usuario del seeder para `/auth/login`).

   Para clientes HTTP (menú o scripts) que llamen rutas protegidas, tras hacer login puedes guardar el token:

   ```env
   API_BASE_URL=http://127.0.0.1:8000
   API_BEARER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

   No subas **`.env`** a Git (ya está en `.gitignore`).

## Base de datos: migraciones y seeder (recomendado)

Con `.env` apuntando a tu PostgreSQL:

```text
py -m alembic upgrade head
py -m scripts.seed
```

Las migraciones son **idempotentes** respecto a tablas ya creadas con `init_db.py`: no vuelven a crear `juegos` ni duplican columnas; solo registran el estado en `alembic_version` y aplican lo que falte (`telefono`, `api_usuarios`).

Alternativa rápida solo con ORM (desarrollo):

```text
py init_db.py
```

## Autenticación JWT

1. Arranca la API y abre **Swagger** (`/docs`).
2. **POST `/auth/login`**: cuerpo tipo form (`username` / `password`) con el usuario creado por el seeder (por defecto `admin` y la clave de `SEED_ADMIN_PASSWORD` en `.env`).
3. Copia `access_token` y usa **Authorize** → `Bearer <token>` para probar rutas bajo `/jugadores`, `/juegos`, etc.

Las rutas **`/`** y **`/auth/login`** son públicas; el resto de recursos exige cabecera `Authorization: Bearer ...`.

## CORS

Orígenes permitidos vienen de **`CORS_ORIGINS`** (lista separada por comas). En producción conviene listar solo los dominios del frontend; no uses `*` con `allow_credentials=True`.

## Pruebas locales (pytest)

Tras `alembic upgrade head` y `python -m scripts.seed`:

```text
pytest -q
```

## CI (GitHub Actions)

El workflow **`.github/workflows/ci.yml`** se ejecuta en **push** y **pull_request** hacia la rama **`dev`**: Ruff, Alembic, seeder y pytest contra PostgreSQL de servicio.

## Video de demostración (examen 2)

Demostración del pipeline en GitHub Actions (rama `dev`) y de migraciones/seeder / esquema en base de datos, según el enunciado del examen 2.

**Ver en YouTube:** [https://youtu.be/Vz9pwSoXz44](https://youtu.be/Vz9pwSoXz44)

[![Miniatura – demostración](https://img.youtube.com/vi/Vz9pwSoXz44/0.jpg)](https://youtu.be/Vz9pwSoXz44)

## Video de demostración (examen final)

Demostración de pruebas Pytest, backend desplegado en Render, frontend desplegado en Firebase Hosting y CRUD funcional consumiendo la API desplegada.

**Ver en YouTube:** [https://youtu.be/FGOq7YxQ200](https://youtu.be/FGOq7YxQ200)

[![Miniatura – examen final](https://img.youtube.com/vi/FGOq7YxQ200/0.jpg)](https://youtu.be/FGOq7YxQ200)

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

## Cliente HTTP (`crud_client`)

`crud/crud_client.py` envía **`Authorization: Bearer`** si existe **`API_BEARER_TOKEN`** en el entorno (útil tras login).

## Estructura del proyecto

```text
BACKEND-Sisloterias/
├── app.py
├── main.py
├── alembic/               # Migraciones
├── scripts/seed.py        # Seeder idempotente
├── init_db.py             # create_all (ORM)
├── database/
├── entities/
├── schemas/
├── endpoints/
├── dependencies/          # JWT (get_current_user)
├── crud/
├── core/
├── tests/
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

## Despliegue en Render (examen final)

Guía: [docs/DEPLOY-RENDER.md](docs/DEPLOY-RENDER.md)

Incluye el archivo `render.yaml` (Blueprint). Variables obligatorias en el panel: `DATABASE_URL` (Neon), `SECRET_KEY`, `CORS_ORIGINS` (URLs de Firebase Hosting + `http://localhost:4200`).

El frontend se despliega en **Firebase Hosting** (repo `Frontend-Sisloteria/web`).

## Autor

Proyecto para el curso **Aplicación y Servicios Web**.

Autoras: Valeria y Valentina Sucerquia Alvarez.
