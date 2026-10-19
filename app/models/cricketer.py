"""
SQLAlchemy model = one Postgres table.

class Cricketer(Base) means:
  "this class maps to a real database table"
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.db import Base


class Cricketer(Base):
    __tablename__ = "cricketers"

    # autoincrement=True → Postgres generates id (SERIAL)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    jersey_number: Mapped[int] = mapped_column(Integer, nullable=False)
