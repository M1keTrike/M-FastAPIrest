from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.familia_schema import FamiliaCreate, Familia
from app.controllers.familia_controller import (
    create_familia,
    get_familia,
    get_familias,
    delete_familia,
    update_familia
)
from app.db.database import get_db
from app.utils.jwt_utils import get_current_user  # Importa la función get_current_user

router = APIRouter()

# Proteger la ruta de crear familia
@router.post("/", response_model=Familia)
def create_family(familia: FamiliaCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_familia(db, familia)

# Proteger la ruta de obtener familia por ID
@router.get("/{familia_id}", response_model=Familia)
def read_family(familia_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    familia = get_familia(db, familia_id)
    if familia is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return familia

# Proteger la ruta de obtener todas las familias
@router.get("/", response_model=list[Familia])
def read_families(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_familias(db)

# Proteger la ruta de actualizar familia
@router.put("/{familia_id}", response_model=Familia)
def update_family(familia_id: int, familia: FamiliaCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated_familia = update_familia(db, familia_id, familia.dict())
    if updated_familia is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return updated_familia

# Proteger la ruta de eliminar familia
@router.delete("/{familia_id}")
def delete_family(familia_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return delete_familia(db, familia_id)
