# FastAPI Monolithic Boilerplate

A production-friendly **FastAPI modular monolith** boilerplate.

It is a single deployable application, but code is organized by feature modules so it can grow without becoming a tangled single-file API.

## Features

- FastAPI
- Python 3.12+
- Pydantic v2
- Pydantic Settings
- Uvicorn ASGI server
- Modular-monolith structure
- Router → service → repository pattern
- Health endpoint
- Users example module
- In-memory repository
- Centralized exception handling
- Consistent JSON response envelope
- Request ID middleware
- Security headers middleware
- CORS configuration
- Pytest + FastAPI TestClient tests
- Ruff linting/formatting
- Mypy type checking
- Dockerfile
- Docker Compose
- Codex-friendly `AGENTS.md`

## Project structure

```txt
fastapi-python-monolithic-boilerplate/
├─ app/
│  ├─ main.py
│  ├─ api/
│  │  └─ router.py
│  ├─ common/
│  │  ├─ errors.py
│  │  ├─ exception_handlers.py
│  │  ├─ responses.py
│  │  └─ middleware/
│  ├─ core/
│  │  ├─ config.py
│  │  └─ logging.py
│  └─ modules/
│     ├─ root/
│     ├─ health/
│     └─ users/
├─ tests/
├─ http/
├─ pyproject.toml
├─ Dockerfile
├─ docker-compose.yml
├─ Makefile
└─ README.md
```

## Requirements

- Python 3.12+
- pip

## Local setup

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
cp .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Run development server

```bash
make dev
```

Or directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

```txt
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/api/v1/users
http://localhost:8000/api/v1/docs
```

## Test

```bash
pytest
```

Or:

```bash
make test
```

## Lint, format, and type-check

```bash
make lint
make format
make typecheck
make check
```

## Docker

```bash
docker compose up --build
```

## API routes

```txt
GET    /                         Root metadata
GET    /health                   Health check
GET    /api/v1/users             List users
POST   /api/v1/users             Create user
GET    /api/v1/users/{user_id}   Get user by ID
PATCH  /api/v1/users/{user_id}   Update user
DELETE /api/v1/users/{user_id}   Delete user
GET    /api/v1/docs              Swagger UI
GET    /api/v1/redoc             ReDoc
GET    /api/v1/openapi.json      OpenAPI JSON
```

## Example request

```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "content-type: application/json" \
  -d '{"name":"Ada Lovelace","email":"ada@example.com"}'
```

## Response format

Success:

```json
{
  "ok": true,
  "data": {},
  "requestId": "..."
}
```

Error:

```json
{
  "ok": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "The requested endpoint was not found."
  },
  "requestId": "..."
}
```

## Adding a new module

Create a new folder under `app/modules/<feature>/`:

```txt
app/modules/orders/
├─ router.py
├─ schemas.py
├─ models.py
├─ repository.py
└─ service.py
```

Then include the module router in `app/api/router.py`.

## Database integration

The users module uses an in-memory repository so the project runs immediately.

For production, replace:

```txt
app/modules/users/repository.py
```

with a database-backed implementation using SQLAlchemy, SQLModel, Tortoise ORM, Beanie, MongoDB, PostgreSQL, or your preferred persistence layer.

Keep the service layer depending on a repository interface so the HTTP and business logic do not care which database you use.
