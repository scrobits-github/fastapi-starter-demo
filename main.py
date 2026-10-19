"""
Entry point of the FastAPI app.

Run with:
    uv run fastapi dev

Then open:
    http://127.0.0.1:8000/docs   ← interactive Swagger UI (best way to learn)
    http://127.0.0.1:8000/redoc  ← cleaner read-only docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.common.db import init_db
from app.routers import cricketers, health


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Runs once when the server starts / stops.

    Before yield  → startup  (create DB tables if missing)
    After yield   → shutdown
    """
    await init_db()  # init_db is async now
    yield


# FastAPI is a CLASS. Calling FastAPI() creates an APP OBJECT.
app = FastAPI(title="Awesome Project — FastAPI 101", lifespan=lifespan)

app.include_router(health.router)
app.include_router(cricketers.router)
