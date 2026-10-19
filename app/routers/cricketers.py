from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.common.db import get_db
from app.schemas.cricket import Cricket
from app.services import cricketers as service

router = APIRouter(prefix="/cricketers", tags=["cricketers"])


@router.get("/get-all")
async def get_all_cricketers(db: Session = Depends(get_db)):
    cricketers = await service.get_all_cricketers(db)
    if cricketers is False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch cricketers!",
        )
    return {"cricketers": cricketers}


@router.get("/get-one/{id}")
def get_one_cricketer(id: int, db: Session = Depends(get_db)):
    cricketer = service.get_one_cricketer(db, id)
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
def create_cricketer(req: Cricket, db: Session = Depends(get_db)):
    cricketer = service.create_cricketer(db, req)
    if not cricketer:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create cricketer!",
        )
    return {"cricketer": cricketer}
