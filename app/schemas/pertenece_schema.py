from typing import Optional
from pydantic import BaseModel


class PerteneceBase(BaseModel):
    usuario_id: int
    familia_id: Optional[int] = None
    rol: str


class PerteneceCreate(PerteneceBase):
    pass


class Pertenece(PerteneceBase):
    id: int

    class Config:
        orm_mode = True
