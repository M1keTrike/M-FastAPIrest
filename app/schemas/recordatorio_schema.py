from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class NotificacionBase(BaseModel):
    titulo: str
    contenido: str
    fecha_hora: datetime
    evento_id: Optional[int] = None  
    familia_id: Optional[int] = None
    usuario_id: int
    categoria: str
    

class NotificacionCreate(NotificacionBase):
    pass
class NotificacionMail(NotificacionBase):
    correo_destinatario: Optional[EmailStr] = None
class Notificacion(NotificacionBase):
    notificacion_id: int

    class Config:
        orm_mode = True
