# FastAPI 101 — Team Session Guide

Use this talk track with the live project. Run:

```bash
cd awesome-project
uv run fastapi dev
```

Open **http://127.0.0.1:8000/docs** and teach from Swagger.

---

## Session goals (30–45 min)

By the end, the team can:

1. Explain class → object (`app = FastAPI()`)
2. Explain routes + decorators (`@app.get`)
3. Explain packages — with or without `__init__.py` (3.3+ namespace packages)
4. Build a tiny CRUD-ish API with Pydantic + `APIRouter`

---

## Agenda

### 1. What is FastAPI? (3 min)

- Modern Python web framework for APIs
- Built on Starlette (web) + Pydantic (data validation)
- Auto docs at `/docs` (Swagger) and `/redoc`

**Say:** “We write Python functions; FastAPI turns them into HTTP endpoints.”

---

### 2. Class & object refresher (5 min)

```python
app = FastAPI()
```

| Word | Meaning |
|------|---------|
| `FastAPI` | class (blueprint) |
| `FastAPI()` | create object |
| `app` | our application object |

Same idea as `phone = Phone("Apple")`.

**Ask the room:** Is `FastAPI` the object or the class?

---

### 3. Decorator = attach URL to function (5 min)

```python
@router.get("/")
def hello_world():
    return {"message": "Hello, Scrobitsss!"}
```

- `@router.get("/")` is a **decorator** (not a type annotation)
- Means: GET `/` → run `hello_world`
- Return a `dict` → FastAPI sends JSON

**Live demo:** hit `/` and `/health` in `/docs`.

**Ask:** If we open `/`, which function runs?

---

### 4. Packages & `__init__.py` (7 min) ← important

Open the tree:

```text
awesome-project/
  main.py                 ← entry: creates app, includes routers
  app/                    ← package (no __init__.py in this demo)
    schemas/
      cricket.py
    routers/
      health.py
      cricketers.py
```

**Child-level explanation:**

- We import folders like modules: `from app.routers import health`
- That only works if Python treats the folder as a **package**

**Two styles:**

| Style | How |
|-------|-----|
| Classic | Put `__init__.py` in the folder |
| Modern (3.3+) | **Namespace package** — no `__init__.py` needed |

This project uses the modern style (no `__init__.py`). Imports still work:

```python
from app.routers import health
from app.schemas.cricket import Cricket
```

**Why teams often still add `__init__.py`:**

1. Clear intent — “this folder is meant to be imported”
2. Can re-export shortcuts (`from app.schemas import Cricket`)
3. Some tools / older habits expect it

**Tradeoff we hit:** without `schemas/__init__.py`, import the module file:
`from app.schemas.cricket import Cricket` (not `from app.schemas import Cricket`).

**Ask:** Does removing `__init__.py` stop the API on Python 3.13? (Demo: it still runs.)

---

### 5. Pydantic models = request/response shape (7 min)

Open `app/schemas/cricket.py`.

```python
class Cricket(BaseModel):
    first_name: str
    last_name: str
    jersey_number: int
    id: int | None = None  # optional; server fills on create
```

- Client sends JSON → FastAPI validates into `Cricket`
- Bad data (missing field, wrong type) → **422** automatically
- `id` is optional for now (single model). Later you can split Create vs Response models.
- Server sets `id` in the router when creating

**Live demo in `/docs`:**

- POST `/cricketers` with valid body → 201
- POST with `jersey_number: "abc"` → validation error

**Ask:** Who checks the types — us manually, or Pydantic/FastAPI?

---

### 6. Routers = split the API (5 min)

Open `app/routers/cricketers.py` and `main.py`.

```python
router = APIRouter(prefix="/cricketers", tags=["cricketers"])
# ...
app.include_router(cricketers.router)
```

Why:

- Keep `main.py` thin
- Group endpoints by feature
- Tags show up as sections in `/docs`

**Live demo:**

- GET `/cricketers`
- GET `/cricketers/1`
- GET `/cricketers/999` → 404
- POST `/cricketers`

---

### 7. Path params & status codes (3 min)

```python
@router.get("/{cricketer_id}")
def get_cricketer(cricketer_id: int):
    ...
```

- `{cricketer_id}` comes from the URL
- Type `int` → FastAPI converts/validates
- `HTTPException(404)` → proper error JSON

---

### 8. How to run (2 min)

```bash
uv run fastapi dev          # hot reload, from project root
# or
uv run uvicorn main:app --reload
```

`main:app` = file `main.py`, variable `app`.

---

## Cheat sheet (leave on screen)

| Concept | Example |
|---------|---------|
| App object | `app = FastAPI()` |
| Decorator / route | `@router.get("/")` |
| Package | folder importable; `__init__.py` optional on 3.3+ |
| Data shape | `class Cricket(BaseModel)` |
| Route group | `APIRouter` + `include_router` |
| Auto docs | `/docs` |
| Validation error | HTTP 422 |
| Not found | `HTTPException(404)` |

---

## Postgres + layers (extra wow — 5 min)

We replaced the in-memory list with real Postgres.

```bash
docker compose up -d          # start DB on localhost:5433
uv run fastapi dev            # API talks to Postgres
```

| Folder | Job |
|--------|-----|
| `common/` | DB URL + engine + `get_db` session |
| `models/` | SQLAlchemy table (`Cricketer`) |
| `services/` | list / get / create in DB |
| `routers/` | HTTP only; calls services |
| `schemas/` | JSON shape (Pydantic) |

**id now:** Postgres `SERIAL` / autoincrement — no `_next_id` counter.

**Say:** “Router doesn’t talk SQL. Service does. Common holds the connection.”

---

## Hands-on for the team (optional 10 min)

Ask them to add:

1. `DELETE /cricketers/{id}`
2. Or a new field `team: str` on `Cricket`

Then restart isn’t needed (`fastapi dev` reloads).

---

## Talking points if someone asks…

**“Is `__init__` the same as `__init__.py`?”**  
No.

- `__init__` method → constructor inside a **class**
- `__init__.py` file → classic way to mark a **folder** as a package (optional on 3.3+)

**“Why not put everything in `main.py`?”**  
Fine for hello-world. Painful for real apps. Packages + routers scale.

**“Annotation vs decorator?”**

- Annotation: `name: str`
- Decorator: `@app.get("/")`

---

## Wow facts & gotchas (tell the team — saves hours later)

### 1. `__pycache__/` — “Who made these folders?!”

- Python auto-creates `__pycache__` when you import modules
- It stores `.pyc` = **compiled bytecode** (faster next import)
- You did not create it — Python did
- **Never commit it** — add to `.gitignore`
- Safe to delete anytime; Python recreates it

**Say:** “It’s Python’s speed cache, not your source code.”

---

### 2. `.venv/` — your project’s private Python

- Virtual env = isolated packages for **this** project only
- `uv` creates/uses `.venv` automatically
- Don’t install FastAPI globally “for everything”
- Don’t commit `.venv` either

---

### 3. `uv.lock` — why versions don’t break on teammate’s laptop

- `pyproject.toml` = what you want (`fastapi>=...`)
- `uv.lock` = exact versions that actually got installed
- Commit **both** so everyone runs the same stack

---

### 4. `main:app` means something precise

```bash
uvicorn main:app --reload
#        ^     ^
#     file   variable name inside that file
```

If you rename `app = FastAPI()` to `application = FastAPI()`, you must run `main:application`.

---

### 5. Docs are free — and you can turn them off

| Path | What |
|------|------|
| `/docs` | Swagger UI (try APIs) |
| `/redoc` | ReDoc (pretty read-only) |
| `/openapi.json` | Machine-readable API schema |

In production many teams disable `/docs`. For 101, leave them on — they’re the best teacher.

---

### 6. Status codes you’ll see a lot

| Code | Meaning | When in our app |
|------|---------|-----------------|
| 200 | OK | GET success |
| 201 | Created | POST success |
| 404 | Not found | Wrong id |
| 422 | Validation error | Bad JSON / wrong types (Pydantic) |
| 500 | Server bug | Unhandled exception in your code |

**Wow line:** “422 is usually *your client data*, 500 is usually *your code*.”

---

### 7. In-memory DB resets on restart

Our `_db` list in `cricketers.py` lives in RAM.  
Restart server → data gone.  
That’s normal for a demo — real apps use Postgres/etc.

---

### 8. Hot reload is magic (and a trap)

`fastapi dev` / `--reload` restarts when files change.  
**Trap:** if you store data in memory, reload wipes it.  
Also: syntax error in a file can stop reload until you fix it.

---

### 9. `self` vs `__init__.py` vs `__pycache__` (clear the names)

| Name | What |
|------|------|
| `self` | “this object” inside a class method |
| `__init__` | constructor method of a class |
| `__init__.py` | optional package marker file (classic style) |
| `__pycache__` | auto cache folder of `.pyc` files |

Three different `__` things — don’t mix them up.

---

### 10. Type hints are not just decoration in FastAPI

```python
def get_cricketer(cricketer_id: int):
```

FastAPI **uses** that `int` to:
- parse the path param
- show it in `/docs`
- reject `"abc"` with 422

Same for Pydantic models on POST bodies.

---

### 11. Order of path routes can matter

```python
@router.get("/{cricketer_id}")   # catches almost anything
@router.get("/me")               # may never be reached if defined after
```

Put **specific** paths (`/me`) **before** dynamic ones (`/{id}`).

---

### 12. CORS will confuse frontend people later

Browser calls from `localhost:3000` → API on `localhost:8000` need CORS.  
Not needed when you only use `/docs`. Mention it so day-2 isn’t a surprise:

```python
from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(CORSMiddleware, ...)
```

---

### 13. Async `async def` vs normal `def`

- `def` → FastAPI runs it in a threadpool (fine for beginners)
- `async def` → for async I/O (DB/http libraries that support await)
- **Don’t** put heavy blocking `time.sleep` / sync DB calls inside `async def` without care

For 101: `def` is totally OK.

---

### 14. What to put in `.gitignore` (show this)

```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
.env
```

`.env` often has secrets — never commit.

---

### Quick “wow” demo order in the session

1. Show `__pycache__` appears after first run → delete it → run again → comes back  
2. Break POST body type → show **422** in `/docs`  
3. Hit bad id → show **404**  
4. Open `/redoc` and `/openapi.json`  
5. Restart server → POST data gone (in-memory)
