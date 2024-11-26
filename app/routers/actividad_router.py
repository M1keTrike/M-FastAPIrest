from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.actividad_schema import ActividadCreate, Actividad
from app.controllers.actividad_controller import (
    create_actividad,
    get_actividad,
    get_actividades,
    delete_actividad,
    update_actividad,
    get_actividades_by_user_id,
)
from app.db.database import get_db
from app.utils.jwt_utils import get_current_user  # Importa la función get_current_user

router = APIRouter()

# Proteger la ruta de crear actividad
@router.post("/", response_model=Actividad)
def create_activity(actividad: ActividadCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_actividad(db, actividad)

# Proteger la ruta de obtener actividad por ID
@router.get("/{actividad_id}", response_model=Actividad)
def read_activity(actividad_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    actividad = get_actividad(db, actividad_id)
    if actividad is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return actividad

# Proteger la ruta de obtener todas las actividades
@router.get("/", response_model=list[Actividad])
def read_activities(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_actividades(db)

# Proteger la ruta de actualizar actividad
@router.put("/{actividad_id}", response_model=Actividad)
def update_activity(actividad_id: int, actividad: ActividadCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated_actividad = update_actividad(db, actividad_id, actividad.dict())
    if updated_actividad is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated_actividad

# Proteger la ruta de eliminar actividad
@router.delete("/{actividad_id}")
def delete_activity(actividad_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return delete_actividad(db, actividad_id)

# Proteger la ruta de obtener actividades por usuario
@router.get("/user/{usuario_id}", response_model=list[Actividad])
def read_activities_by_user(usuario_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    actividades = get_actividades_by_user_id(db, usuario_id)
    if not actividades:
        raise HTTPException(status_code=404, detail="No activities found for the given user")
    return actividades
