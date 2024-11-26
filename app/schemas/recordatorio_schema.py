from pydantic import BaseModel, EmailStr, conlist
from typing import Optional, List
from datetime import datetime

# Schema for creating a new notification
class NotificacionCreate(BaseModel):
    titulo: str
    contenido: str
    fecha_hora: datetime
    evento_id: Optional[int] = None  # Optional, as the model suggests
    familia_id: Optional[int] = None
    usuario_id: int  # Required
    categoria: str
    correo_destinatario: Optional[List[EmailStr]] = None  # List of valid email addresses

    class Config:
        orm_mode = True  # To work seamlessly with SQLAlchemy models


# Schema for updating an existing notification
class NotificacionUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    fecha_hora: Optional[datetime] = None
    evento_id: Optional[int] = None
    familia_id: Optional[int] = None
    usuario_id: Optional[int] = None
    categoria: Optional[str] = None
    correo_destinatario: Optional[List[EmailStr]] = None

    class Config:
        orm_mode = True


# Schema for notification response, including id
class NotificacionResponse(BaseModel):
    notificacion_id: int
    titulo: str
    contenido: str
    fecha_hora: datetime
    evento_id: Optional[int]
    familia_id: Optional[int]
    usuario_id: int
    categoria: str
    correo_destinatario: Optional[List[EmailStr]] = None

    class Config:
        orm_mode = True
