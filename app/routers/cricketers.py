"""
HTTP layer for cricketers (async).

Rule of thumb:
  routers  → talk HTTP (status codes, request/response)
  services → talk database

Because services are async, routes are `async def` and we `await` them.

Depends(get_db) = FastAPI opens an AsyncSession, gives it to us,
and closes it after the request.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.db import get_db
from app.schemas.cricket import Cricket
from app.services import cricketers as service

router = APIRouter(prefix="/cricketers", tags=["cricketers"])


@router.get("/get-all")
async def get_all_cricketers(db: AsyncSession = Depends(get_db)):
    """GET /cricketers/get-all → list everyone."""
    # await = "pause this request until the DB work finishes"
    # meanwhile FastAPI can handle other requests
    cricketers = await service.get_all_cricketers(db)
    if cricketers is False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch cricketers!",
        )
    return {"cricketers": cricketers}


@router.get("/get-one/{id}")
async def get_one_cricketer(id: int, db: AsyncSession = Depends(get_db)):
    """GET /cricketers/get-one/1

    {id} is a PATH PARAMETER.
    Type hint `id: int` → FastAPI parses/validates it (bad value → 422).
    """
    cricketer = await service.get_one_cricketer(db, id)
    if cricketer is False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch cricketer!",
        )
    if cricketer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cricketer Not Found!",
        )
    return {"cricketer": cricketer}


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_cricketer(req: Cricket, db: AsyncSession = Depends(get_db)):
    """POST /cricketers/create

    req: Cricket → JSON body validated by Pydantic (bad body → 422).
    201 = created.
    """
    cricketer = await service.create_cricketer(db, req)
    if not cricketer:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create cricketer!",
        )
    return {"cricketer": cricketer}
