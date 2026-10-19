from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cricketer import Cricketer
from app.schemas.cricket import Cricket


def get_all_cricketers(db: Session) -> list[Cricketer] | bool:
    try:
        return list(db.scalars(select(Cricketer).order_by(Cricketer.id)).all())
    except Exception as e:
        print(e)
        return False


def get_one_cricketer(db: Session, id: int) -> Cricketer | None | bool:
    try:
        return db.get(Cricketer, id)
    except Exception as e:
        print(e)
        return False


def create_cricketer(db: Session, data: Cricket) -> Cricketer | bool:
    try:
        row = Cricketer(
            first_name=data.first_name,
            last_name=data.last_name,
            jersey_number=data.jersey_number,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row
    except Exception as e:
        print(e)
        db.rollback()
        return False
