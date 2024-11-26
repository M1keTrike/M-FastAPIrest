from sqlalchemy.orm import Session
from app.models.actividad_model import Actividad
from app.schemas.actividad_schema import ActividadCreate

def create_actividad(db: Session, actividad_data: ActividadCreate):
    db_actividad = Actividad(**actividad_data.dict())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

def get_actividad(db: Session, actividad_id: int):
    return db.query(Actividad).filter(Actividad.actividad_id == actividad_id).first()

def get_actividades(db: Session):
    return db.query(Actividad).all()

def delete_actividad(db: Session, actividad_id: int):
    actividad = get_actividad(db, actividad_id)
    db.delete(actividad)
    db.commit()
    return {"message": "Activity deleted successfully"}

def update_actividad(db: Session, actividad_id: int, actividad_data: dict):
    actividad = get_actividad(db, actividad_id)
    if not actividad:
        return None
    for key, value in actividad_data.items():
        setattr(actividad, key, value)
    db.commit()
    db.refresh(actividad)
    return actividad

def get_actividades_by_user_id(db: Session, usuario_id: int):
    return db.query(Actividad).filter(Actividad.usuario_id == usuario_id).all()

