from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.evento_schema import EventoCreate, Evento
from app.controllers.evento_controller import create_evento, get_evento, get_eventos, delete_evento, update_evento, get_eventos_by_familia_id
from app.db.database import get_db
# Importa la dependencia para verificar el usuario autenticado
from app.utils.jwt_utils import get_current_user
# Importa el modelo Usuario para tipado
from app.models.usuario_model import Usuario

router = APIRouter()

# Proteger la ruta de creación de evento


@router.post("/", response_model=Evento)
def create_event(evento: EventoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    # Puedes utilizar `current_user` si necesitas comprobar permisos o asociar el evento al usuario
    return create_evento(db, evento)


# Proteger la ruta para obtener un evento específico
@router.get("/{evento_id}", response_model=Evento)
def read_event(evento_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    evento = get_evento(db, evento_id)
    if evento is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return evento


# Proteger la ruta para obtener todos los eventos
@router.get("/", response_model=list[Evento])
def read_events(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return get_eventos(db)


# Proteger la ruta de actualización de evento
@router.put("/{evento_id}", response_model=Evento)
def update_event(evento_id: int, evento: EventoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    updated_event = update_evento(db, evento_id, evento.dict())
    if updated_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event


# Proteger la ruta de eliminación de evento
@router.delete("/{evento_id}")
def delete_event(evento_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return delete_evento(db, evento_id)


# Proteger la ruta para obtener eventos por familia
@router.get("/familia/{familia_id}", response_model=list[Evento])
def read_events_by_familia_id(familia_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    eventos = get_eventos_by_familia_id(db, familia_id)
    if not eventos:
        raise HTTPException(
            status_code=404, detail="No events found for this family ID")
    return eventos
