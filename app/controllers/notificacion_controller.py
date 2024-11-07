from sqlalchemy.orm import Session
from app.models.notificacion_model import Notificacion
from app.schemas.notificacion_schema import NotificacionCreate

def create_notificacion(db: Session, notificacion_data: NotificacionCreate):
    db_notificacion = Notificacion(**notificacion_data.dict())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

def get_notificacion(db: Session, notificacion_id: int):
    return db.query(Notificacion).filter(Notificacion.notificacion_id == notificacion_id).first()

def get_notificaciones(db: Session):
    return db.query(Notificacion).all()

def delete_notificacion(db: Session, notificacion_id: int):
    notificacion = get_notificacion(db, notificacion_id)
    db.delete(notificacion)
    db.commit()
    return {"message": "Notification deleted successfully"}

def update_notificacion(db: Session, notificacion_id: int, notificacion_data: dict):
    notificacion = get_notificacion(db, notificacion_id)
    if not notificacion:
        return None
    for key, value in notificacion_data.items():
        setattr(notificacion, key, value)
    db.commit()
    db.refresh(notificacion)
    return notificacion
