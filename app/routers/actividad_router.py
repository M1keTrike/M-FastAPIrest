from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.actividad_schema import ActividadCreate, Actividad
from app.controllers.actividad_controller import create_actividad, get_actividad, get_actividades, delete_actividad, update_actividad
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=Actividad)
def create_activity(actividad: ActividadCreate, db: Session = Depends(get_db)):
    return create_actividad(db, actividad)

@router.get("/{actividad_id}", response_model=Actividad)
def read_activity(actividad_id: int, db: Session = Depends(get_db)):
    actividad = get_actividad(db, actividad_id)
    if actividad is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return actividad

@router.get("/", response_model=list[Actividad])
def read_activities(db: Session = Depends(get_db)):
    return get_actividades(db)

@router.put("/{actividad_id}", response_model=Actividad)
def update_activity(actividad_id: int, actividad: ActividadCreate, db: Session = Depends(get_db)):
    updated_actividad = update_actividad(db, actividad_id, actividad.dict())
    if updated_actividad is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated_actividad

@router.delete("/{actividad_id}")
def delete_activity(actividad_id: int, db: Session = Depends(get_db)):
    return delete_actividad(db, actividad_id)
