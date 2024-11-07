from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.familia_schema import FamiliaCreate, Familia
from app.controllers.familia_controller import create_familia, get_familia, get_familias, delete_familia, update_familia
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=Familia)
def create_family(familia: FamiliaCreate, db: Session = Depends(get_db)):
    return create_familia(db, familia)

@router.get("/{familia_id}", response_model=Familia)
def read_family(familia_id: int, db: Session = Depends(get_db)):
    familia = get_familia(db, familia_id)
    if familia is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return familia

@router.get("/", response_model=list[Familia])
def read_families(db: Session = Depends(get_db)):
    return get_familias(db)

@router.put("/{familia_id}", response_model=Familia)
def update_family(familia_id: int, familia: FamiliaCreate, db: Session = Depends(get_db)):
    updated_familia = update_familia(db, familia_id, familia.dict())
    if updated_familia is None:
        raise HTTPException(status_code=404, detail="Family not found")
    return updated_familia

@router.delete("/{familia_id}")
def delete_family(familia_id: int, db: Session = Depends(get_db)):
    return delete_familia(db, familia_id)
