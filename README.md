# Awesome Project — FastAPI 101

A beginner-friendly FastAPI + Postgres example.

Learn by reading the comments in the code, then try the live docs at `/docs`.

## Quick start

Needs: [uv](https://docs.astral.sh/uv/) and [Docker](https://docs.docker.com/get-docker/).

```bash
# 1) Start Postgres
docker compose up -d

# 2) Env file (optional — defaults match docker-compose)
cp .env.example .env

# 3) Run the API (hot reload)
uv run fastapi dev
```

| URL | What |
|-----|------|
| http://127.0.0.1:8000 | App |
| http://127.0.0.1:8000/docs | Swagger UI (try APIs here) |
| http://127.0.0.1:8000/redoc | ReDoc |
| `localhost:5433` | Postgres (`awesome` / `awesome` / `awesome`) |

## Project layout

```text
main.py                 # creates the FastAPI app, includes routers
docker-compose.yml      # Postgres
.env.example            # sample DATABASE_URL
uv.lock                 # locked dependency versions (commit this)
app/
  common/               # settings + DB engine/session
  models/               # SQLAlchemy tables (Postgres)
  schemas/              # Pydantic models (JSON in/out)
  routers/              # HTTP endpoints
  services/             # DB operations used by routers
SESSION.md              # longer teaching talk track
```

## How a request flows

```text
HTTP request
   → router   (status codes, Depends, validation)
   → service  (SQLAlchemy queries)
   → Postgres
   → JSON response
```

| Layer | Job |
|-------|-----|
| `routers/` | HTTP only |
| `services/` | list / get / create in DB |
| `models/` | table mapping |
| `schemas/` | request/response shape + validation |
| `common/` | `DATABASE_URL`, engine, `get_db` |

## API endpoints

| Method | Path | What |
|--------|------|------|
| GET | `/` | Hello |
| GET | `/health` | Health check |
| GET | `/cricketers/get-all` | List all |
| GET | `/cricketers/get-one/{id}` | Get one (404 if missing) |
| POST | `/cricketers/create` | Create (`id` from Postgres) |

### Example create body

```json
{
  "first_name": "Virat",
  "last_name": "Kohli",
  "jersey_number": 18
}
```

## Concepts this repo teaches

1. **Class vs object** — `app = FastAPI()`
2. **Decorators** — `@router.get(...)` attaches a URL to a function
3. **Type hints do real work** — FastAPI uses them for parsing, docs, validation
4. **Schema vs model** — Pydantic (API) ≠ SQLAlchemy (DB)
5. **async / await (correct way)** — see section below
6. **Depends + yield** — one DB session per request, then close
7. **Status codes** — 201 create, 404 not found, 422 bad input, 500 server error
8. **`uv.lock`** — commit it so everyone gets the same package versions

## async / await — the correct mental model

`async` is **not** “because we talk to a database.”  
It means: “this function can pause while waiting for I/O, so the server can handle other requests.”

### The full chain (what this repo does)

```text
create_async_engine
   → AsyncSession (get_db)
   → async def service  (await db.execute / commit / refresh)
   → async def router   (await service...)
```

| Layer | Correct async form |
|-------|--------------------|
| Engine | `create_async_engine(...)` |
| Session | `AsyncSession` via `async_sessionmaker` |
| Service | `async def` + `await db.get(...)` / `await db.commit()` |
| Router | `async def` + `await service...` |

### Wrong (crashes)

```python
def get_all(...):           # sync service
    return db.query(...)

async def route(...):
    return await get_all()  # ❌ cannot await a normal function
```

### Right (this project)

```python
async def get_all(db: AsyncSession):
    result = await db.scalars(select(...))
    return list(result.all())

async def route(db: AsyncSession = Depends(get_db)):
    return await get_all(db)  # ✅ awaiting another async function
```

Note: simple routes like `/health` can stay as normal `def` — no DB wait needed.

## Notes for learners

- Tables are auto-created on startup via `await init_db()`. Fine for demos; production should use **Alembic migrations**.
- Folders under `app/` mostly have **no** `__init__.py` (Python 3.3+ namespace packages).
- Best way to explore: open `/docs` and click **Try it out**.

## Learn more

- [FastAPI docs](https://fastapi.tiangolo.com)
- [uv + FastAPI](https://docs.astral.sh/uv/guides/integration/fastapi/)
- Full session script: [SESSION.md](./SESSION.md)
