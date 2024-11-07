from pydantic import BaseModel
from datetime import datetime

class NotificacionBase(BaseModel):
    evento_id: int
    mensaje: str

class NotificacionCreate(NotificacionBase):
    pass

class Notificacion(NotificacionBase):
    notificacion_id: int
    fecha: datetime

    class Config:
        orm_mode = True
