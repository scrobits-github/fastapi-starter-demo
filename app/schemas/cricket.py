from pydantic import BaseModel, ConfigDict


class Cricket(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    jersey_number: int
    id: int | None = None
