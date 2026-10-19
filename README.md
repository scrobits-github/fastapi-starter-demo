# FastAPI 101 — Learn by Building

A small **FastAPI + Postgres** project made for **learners**.

You will build a tiny Cricketers API and understand:

- what FastAPI is doing
- how routes, schemas, models, and services fit together
- how `async` / `await` works **correctly** with a database

No heavy theory first. Run it → click around → read the comments in the code.

---

## What you will have at the end

A working API that can:

| Action | Method + path |
|--------|----------------|
| Say hello | `GET /` |
| Health check | `GET /health` |
| List cricketers | `GET /cricketers/get-all` |
| Get one cricketer | `GET /cricketers/get-one/{id}` |
| Create a cricketer | `POST /cricketers/create` |

Interactive docs (the best teacher): **http://127.0.0.1:8000/docs**

---

## Before you start

Install:

1. [uv](https://docs.astral.sh/uv/) (Python package runner)
2. [Docker](https://docs.docker.com/get-docker/) (for Postgres)

That’s it.

---

## Step 1 — Run the project

```bash
# start Postgres
docker compose up -d

# optional: copy env file (defaults already match docker-compose)
cp .env.example .env

# start the API with hot reload
uv run fastapi dev
```

Open these in your browser:

| Link | Why open it |
|------|-------------|
| http://127.0.0.1:8000/docs | **Start here** — Try every API |
| http://127.0.0.1:8000/redoc | Cleaner docs to read |
| http://127.0.0.1:8000/health | Quick “is it alive?” check |

Postgres runs on `localhost:5433`  
user / password / database = `awesome` / `awesome` / `awesome`

---

## Step 2 — Try the APIs (5 minutes)

In `/docs`:

1. Open **POST `/cricketers/create`**
2. Click **Try it out**
3. Send this body:

```json
{
  "first_name": "Virat",
  "last_name": "Kohli",
  "jersey_number": 18
}
```

4. Notice: you did **not** send `id` — Postgres created it  
5. Call **GET `/cricketers/get-all`** — your player should appear  
6. Call **GET `/cricketers/get-one/1`** — one player  
7. Call **GET `/cricketers/get-one/999999`** — you should get **404**

If that worked, the app is fine. Now learn *why*.

---

## Step 3 — Read the code in this order

Read files **top to bottom** like a story:

| Order | File | What you learn |
|------:|------|----------------|
| 1 | `main.py` | App object, lifespan, include routers |
| 2 | `app/routers/health.py` | Simplest route + decorator |
| 3 | `app/routers/cricketers.py` | Real API routes, status codes, `Depends`, `await` |
| 4 | `app/schemas/cricket.py` | Pydantic = JSON shape / validation |
| 5 | `app/models/cricketer.py` | SQLAlchemy = Postgres table |
| 6 | `app/services/cricketers.py` | DB create / list / get |
| 7 | `app/common/db.py` | Async engine, session, `get_db`, `init_db` |
| 8 | `app/common/config.py` | Settings from `.env` |

Every important file has **learner comments** inside.

---

## Mental model (keep this picture)

```text
Browser /docs
    ↓
Router   (HTTP: path, status code, validation)
    ↓
Service  (talks to database)
    ↓
Postgres
    ↓
JSON response
```

| Folder | Job (one line) |
|--------|----------------|
| `routers/` | HTTP only |
| `services/` | Database operations |
| `schemas/` | Request/response JSON (Pydantic) |
| `models/` | Database tables (SQLAlchemy) |
| `common/` | Config + DB connection |

**Schema ≠ model**

- Schema → how data looks in the API  
- Model → how data is stored in Postgres  

---

## async / await (explained simply)

### What `await` means

> “Pause this request until the slow I/O finishes.  
> Meanwhile FastAPI can handle other requests.”

### The correct chain (this repo)

```text
create_async_engine
  → AsyncSession
  → async def service   (await db.get / commit)
  → async def router    (await service...)
```

### Wrong vs right

```python
# ❌ WRONG — cannot await a normal function
def get_all(db):
    return ...

async def route(db):
    return await get_all(db)   # crash


# ✅ RIGHT — both sides are async
async def get_all(db: AsyncSession):
    result = await db.scalars(select(...))
    return list(result.all())

async def route(db: AsyncSession = Depends(get_db)):
    return await get_all(db)
```

`/health` stays a normal `def` on purpose — no database wait, so no need for async there.

---

## Tiny glossary

| Word | Meaning |
|------|---------|
| `app = FastAPI()` | Create the app **object** from the FastAPI **class** |
| `@router.get(...)` | **Decorator** — attach a URL to a function |
| Type hints (`id: int`) | FastAPI uses them for parsing + docs + validation |
| `Depends(get_db)` | Give this route a DB session, then close it |
| `HTTP_404_NOT_FOUND` | Resource missing |
| `HTTP_422` | Bad input (validation failed) |
| `HTTP_201_CREATED` | Created successfully |
| `uv.lock` | Exact package versions — **commit this** |
| `__pycache__/` | Python speed cache — ignore it, don’t commit |
| `init_db()` | Auto-create tables on startup (demo style) |

---

## Suggested learning path (if you are new)

1. Run the app and play in `/docs` (15 min)  
2. Read `main.py` + `health.py` (10 min)  
3. Read `cricketers` router + schema (15 min)  
4. Read model + service + `db.py` (20 min)  
5. Break something on purpose (rename a field) and watch `/docs` / errors  

Optional deep talk track for workshops: [SESSION.md](./SESSION.md)

---

## Project tree

```text
main.py                 # start here
docker-compose.yml      # Postgres
.env.example            # sample DATABASE_URL
uv.lock                 # locked deps (commit this)
app/
  routers/              # HTTP endpoints
  services/             # DB logic
  schemas/              # Pydantic (API shapes)
  models/               # SQLAlchemy (tables)
  common/               # settings + async DB setup
SESSION.md              # longer workshop script
```

---

## Good to know

- Tables are created automatically on startup (`init_db`). Great for learning. Real production apps usually use **Alembic migrations**.
- `.env` is secret → not committed. Use `.env.example` as the template.
- `.venv/` is local → not committed.
- This repo prefers **clear code + comments** over clever tricks.

---

## Learn more

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [uv + FastAPI](https://docs.astral.sh/uv/guides/integration/fastapi/)
- Workshop script: [SESSION.md](./SESSION.md)

---

Happy learning. Open `/docs`, click **Try it out**, then come back and read the code.  
That’s the FastAPI way.
