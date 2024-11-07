from sqlalchemy.orm import Session
from app.models.recordatorio_model import Recordatorio
from app.schemas.recordatorio_schema import RecordatorioCreate

def create_recordatorio(db: Session, recordatorio_data: RecordatorioCreate):
    db_recordatorio = Recordatorio(**recordatorio_data.dict())
    db.add(db_recordatorio)
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

def get_recordatorio(db: Session, recordatorio_id: int):
    return db.query(Recordatorio).filter(Recordatorio.recordatorio_id == recordatorio_id).first()

def get_recordatorios(db: Session):
    return db.query(Recordatorio).all()

def delete_recordatorio(db: Session, recordatorio_id: int):
    recordatorio = get_recordatorio(db, recordatorio_id)
    db.delete(recordatorio)
    db.commit()
    return {"message": "Reminder deleted successfully"}

def update_recordatorio(db: Session, recordatorio_id: int, recordatorio_data: dict):
    recordatorio = get_recordatorio(db, recordatorio_id)
    if not recordatorio:
        return None
    for key, value in recordatorio_data.items():
        setattr(recordatorio, key, value)
    db.commit()
    db.refresh(recordatorio)
    return recordatorio
