from pydantic import BaseModel
from datetime import date
from typing import Optional

class EventoBase(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    familia_id: int

class EventoCreate(EventoBase):
    pass

class Evento(EventoBase):
    evento_id: int

    class Config:
        orm_mode = True
