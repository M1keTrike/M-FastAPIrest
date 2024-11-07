from pydantic import BaseModel
from datetime import time
from typing import Optional

class RecordatorioBase(BaseModel):
    contenido: str
    id_familia: int
    hora_limite: Optional[time] = None

class RecordatorioCreate(RecordatorioBase):
    pass

class Recordatorio(RecordatorioBase):
    recordatorio_id: int

    class Config:
        orm_mode = True
