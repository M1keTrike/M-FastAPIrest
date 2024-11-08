from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.notificacion_schema import NotificacionCreate, Notificacion
from app.controllers.notificacion_controller import create_notificacion, get_notificacion, get_notificaciones, delete_notificacion, update_notificacion
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=Notificacion)
def create_notification(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    return create_notificacion(db, notificacion)

@router.get("/{notificacion_id}", response_model=Notificacion)
def read_notification(notificacion_id: int, db: Session = Depends(get_db)):
    notificacion = get_notificacion(db, notificacion_id)
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notificacion

@router.get("/", response_model=list[Notificacion])
def read_notifications(db: Session = Depends(get_db)):
    return get_notificaciones(db)

@router.put("/{notificacion_id}", response_model=Notificacion)
def update_notification(notificacion_id: int, notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    updated_notificacion = update_notificacion(db, notificacion_id, notificacion.dict())
    if updated_notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notificacion

@router.delete("/{notificacion_id}")
def delete_notification(notificacion_id: int, db: Session = Depends(get_db)):
    return delete_notificacion(db, notificacion_id)
