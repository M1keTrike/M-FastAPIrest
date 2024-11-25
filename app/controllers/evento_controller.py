from sqlalchemy.orm import Session
from app.models.evento_model import Evento
from app.schemas.evento_schema import EventoCreate

def create_evento(db: Session, evento_data: EventoCreate):
    db_evento = Evento(**evento_data.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def get_evento(db: Session, evento_id: int):
    return db.query(Evento).filter(Evento.evento_id == evento_id).first()

def get_eventos(db: Session):
    return db.query(Evento).all()

def delete_evento(db: Session, evento_id: int):
    evento = get_evento(db, evento_id)
    db.delete(evento)
    db.commit()
    return {"message": "Event deleted successfully"}

def update_evento(db: Session, evento_id: int, evento_data: dict):
    evento = get_evento(db, evento_id)
    if not evento:
        return None
    for key, value in evento_data.items():
        setattr(evento, key, value)
    db.commit()
    db.refresh(evento)
    return evento

def get_eventos_by_familia_id(db: Session, familia_id: int):
    return db.query(Evento).filter(Evento.familia_id == familia_id).all()

