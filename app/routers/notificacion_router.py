from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.notificacion_schema import NotificacionCreate, Notificacion
from app.controllers.notificacion_controller import (
    create_notificacion,
    get_notificacion,
    get_notificaciones,
    delete_notificacion,
    update_notificacion
)
from app.db.database import get_db
from app.utils.jwt_utils import get_current_user  # Importa la función get_current_user

router = APIRouter()

# Ruta pública para crear una notificación (sin autenticación)
@router.post("/", response_model=Notificacion)
def create_notification(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    return create_notificacion(db, notificacion)

# Proteger la ruta de obtener notificación por ID
@router.get("/{notificacion_id}", response_model=Notificacion)
def read_notification(notificacion_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    notificacion = get_notificacion(db, notificacion_id)
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notificacion

# Proteger la ruta de obtener todas las notificaciones
@router.get("/", response_model=list[Notificacion])
def read_notifications(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_notificaciones(db)

# Proteger la ruta de actualizar notificación
@router.put("/{notificacion_id}", response_model=Notificacion)
def update_notification(notificacion_id: int, notificacion: NotificacionCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated_notificacion = update_notificacion(db, notificacion_id, notificacion.dict())
    if updated_notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notificacion

# Proteger la ruta de eliminar notificación
@router.delete("/{notificacion_id}")
def delete_notification(notificacion_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return delete_notificacion(db, notificacion_id)
