from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class ActividadBase(BaseModel):
    nombre: str
    fecha_inicio: date
    hora_inicio: time
    fecha_fin: Optional[date] = None
    hora_fin: Optional[time] = None
    categoria: Optional[str] = None
    usuario_id: int  

class ActividadCreate(ActividadBase):
    pass

class Actividad(ActividadBase):
    actividad_id: int

    class Config:
        orm_mode = True
