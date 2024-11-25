from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.evento_schema import EventoCreate, Evento
from app.controllers.evento_controller import create_evento, get_evento, get_eventos, delete_evento, update_evento, get_eventos_by_familia_id
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=Evento)
def create_event(evento: EventoCreate, db: Session = Depends(get_db)):
    return create_evento(db, evento)


@router.get("/{evento_id}", response_model=Evento)
def read_event(evento_id: int, db: Session = Depends(get_db)):
    evento = get_evento(db, evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return evento


@router.get("/", response_model=list[Evento])
def read_events(db: Session = Depends(get_db)):
    return get_eventos(db)


@router.put("/{evento_id}", response_model=Evento)
def update_event(evento_id: int, evento: EventoCreate, db: Session = Depends(get_db)):
    updated_event = update_evento(db, evento_id, evento.dict())
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event


@router.delete("/{evento_id}")
def delete_event(evento_id: int, db: Session = Depends(get_db)):
    return delete_evento(db, evento_id)


@router.get("/familia/{familia_id}", response_model=list[Evento])
def read_events_by_familia_id(familia_id: int, db: Session = Depends(get_db)):
    eventos = get_eventos_by_familia_id(db, familia_id)
    if not eventos:
        raise HTTPException(
            status_code=404, detail="No events found for this family ID")
    return eventos
