from pydantic import BaseModel
from typing import Optional


class PerteneceCreate(BaseModel):
    usuario_id: int
    familia_id: Optional[int]
    rol: str


class PerteneceResponse(BaseModel):
    id: int
    usuario_id: int
    familia_id: Optional[int]
    rol: str

    class Config:
        from_attributes = True
