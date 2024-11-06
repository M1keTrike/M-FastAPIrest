from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal

class ActivityCreate(BaseModel):
    title: str
    priority: Literal['alta', 'media', 'baja']
    state: Literal['pendiente', 'en_progreso', 'completada', 'cancelada']
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: int

class Activity(BaseModel):
    id: int
    title: str
    priority: Literal['alta', 'media', 'baja']
    state: Literal['pendiente', 'en_progreso', 'completada', 'cancelada']
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: int
