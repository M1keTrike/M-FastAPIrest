from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class RecordatorioCreate(BaseModel):
    title: str
    date_hour: datetime
    repetition: Optional[Literal['diaria', 'semanal', 'mensual', 'anual', 'ninguna']] = 'ninguna'
    state: Optional[Literal['activo', 'inactivo']] = 'activo'
    aditional_note: Optional[str]
    activity_id: int

class Recordatorio(BaseModel):
    id: int
    title: str
    date_hour: datetime
    repetition: Optional[Literal['diaria', 'semanal', 'mensual', 'anual', 'ninguna']] = 'ninguna'
    state: Optional[Literal['activo', 'inactivo']] = 'activo'
    aditional_note: Optional[str]
    activity_id: int
