from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.recordatorio_schema import RecordatorioCreate, Recordatorio
from app.controllers.recordatorio_controller import create_recordatorio, get_recordatorio, get_recordatorios, delete_recordatorio, update_recordatorio
from app.db.database import get_db
from app.utils.jwt_utils import get_current_user  # Importa la función get_current_user

router = APIRouter()

# Ruta pública para crear un recordatorio (sin autenticación)
@router.post("/", response_model=Recordatorio)
def create_reminder(recordatorio: RecordatorioCreate, db: Session = Depends(get_db)):
    return create_recordatorio(db, recordatorio)

# Proteger la ruta de obtener un recordatorio
@router.get("/{recordatorio_id}", response_model=Recordatorio)
def read_reminder(recordatorio_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    recordatorio = get_recordatorio(db, recordatorio_id)
    if recordatorio is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return recordatorio

# Proteger la ruta de obtener todos los recordatorios
@router.get("/", response_model=list[Recordatorio])
def read_reminders(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_recordatorios(db)

# Proteger la ruta de actualizar un recordatorio
@router.put("/{recordatorio_id}", response_model=Recordatorio)
def update_reminder(recordatorio_id: int, recordatorio: RecordatorioCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated_recordatorio = update_recordatorio(db, recordatorio_id, recordatorio.dict())
    if updated_recordatorio is None:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return updated_recordatorio

# Proteger la ruta de eliminar un recordatorio
@router.delete("/{recordatorio_id}")
def delete_reminder(recordatorio_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return delete_recordatorio(db, recordatorio_id)
