"""
Async database wiring (SQLAlchemy 2 + psycopg).

IMPORTANT for learners:
  async/await only works if the WHOLE chain is async:
    create_async_engine → AsyncSession → async def services → await in routers

  You cannot `await` a normal sync function. That crashes.

Pieces:
  engine       → async connection pool to Postgres
  SessionLocal → factory for AsyncSession
  Base         → parent class for ORM table models
  get_db()     → one async session per request
  init_db()    → create tables on startup (demo only)
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.common.config import settings

# Same URL style works with async psycopg:
#   postgresql+psycopg://user:pass@host:port/db
engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """All ORM models inherit from this (see app/models/cricketer.py)."""

    pass


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency — async version.

    yield session  → give DB to the route
    (context exits) → session closes automatically
    """
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    """Create all tables registered on Base (if missing).

    create_all is sync API, so we run it inside run_sync on an async connection.
    Good for demos. Production should use Alembic migrations.
    """
    from app.models.cricketer import Cricketer  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
