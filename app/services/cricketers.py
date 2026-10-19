"""
Async database operations for cricketers.

Every function that hits the DB is `async def` and uses `await`.
That is what makes async/await correct — not the word "database" alone.

Returns:
  - list / row  → success
  - None        → not found (get_one only)
  - False       → error (router turns this into HTTP 500)
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cricketer import Cricketer
from app.schemas.cricket import Cricket


async def get_all_cricketers(db: AsyncSession) -> list[Cricketer] | bool:
    try:
        result = await db.scalars(select(Cricketer).order_by(Cricketer.id))
        return list(result.all())
    except Exception as e:
        print(e)
        return False


async def get_one_cricketer(db: AsyncSession, id: int) -> Cricketer | None | bool:
    try:
        # await because AsyncSession.get is async
        return await db.get(Cricketer, id)
    except Exception as e:
        print(e)
        return False


async def create_cricketer(db: AsyncSession, data: Cricket) -> Cricketer | bool:
    try:
        row = Cricketer(
            first_name=data.first_name,
            last_name=data.last_name,
            jersey_number=data.jersey_number,
        )
        db.add(row)
        await db.commit()      # wait until Postgres saves
        await db.refresh(row)  # wait until id is loaded
        return row
    except Exception as e:
        print(e)
        await db.rollback()
        return False
