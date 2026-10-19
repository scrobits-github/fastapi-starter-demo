"""
Pydantic schema = the JSON shape of the API (request/response).

This is NOT the database table.
  schemas/  → how data looks over HTTP (validation + docs)
  models/   → how data is stored in Postgres
"""

from pydantic import BaseModel, ConfigDict


class Cricket(BaseModel):
    # from_attributes=True lets FastAPI build this schema from an ORM object
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    jersey_number: int
    # Optional on input: client can skip id; Postgres generates it
    id: int | None = None
