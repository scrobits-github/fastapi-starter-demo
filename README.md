# awesome-project — FastAPI 101

Team teaching demo for FastAPI + Postgres.

## Quick start

```bash
# 1) Start Postgres
docker compose up -d

# 2) Run the API
uv run fastapi dev
```

- App: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Postgres: `localhost:5433` (user/pass/db: `awesome`)

Copy `.env.example` → `.env` if needed.

## Teach from

Open **[SESSION.md](./SESSION.md)** — talk track for the session.

## Layout

```text
main.py                 # FastAPI app + lifespan (create tables)
docker-compose.yml      # Postgres
.env                    # DATABASE_URL (not committed)
app/
  common/               # config + db engine/session
  models/               # SQLAlchemy tables
  schemas/              # Pydantic API shapes
  routers/              # HTTP endpoints (thin)
  services/             # DB operations
```

## Who does what

| Layer | Job |
|-------|-----|
| `routers/` | HTTP only — call services |
| `services/` | DB create/list/get |
| `common/` | `DATABASE_URL`, engine, `get_db` |
| `models/` | Postgres table mapping |
| `schemas/` | JSON in/out validation |

## Try the API

| Method | Path | What |
|--------|------|------|
| GET | `/` | Hello |
| GET | `/health` | Health check |
| GET | `/cricketers` | List (from Postgres) |
| GET | `/cricketers/{id}` | One |
| POST | `/cricketers` | Create (`id` from Postgres) |

## Learn more

- [FastAPI docs](https://fastapi.tiangolo.com)
- [uv + FastAPI](https://docs.astral.sh/uv/guides/integration/fastapi/)
