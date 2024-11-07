from sqlalchemy.orm import Session
from app.models.familia_model import Familia
from app.schemas.familia_schema import FamiliaCreate

def create_familia(db: Session, familia_data: FamiliaCreate):
    db_familia = Familia(**familia_data.dict())
    db.add(db_familia)
    db.commit()
    db.refresh(db_familia)
    return db_familia

def get_familia(db: Session, familia_id: int):
    return db.query(Familia).filter(Familia.id_familia == familia_id).first()

def get_familias(db: Session):
    return db.query(Familia).all()

def delete_familia(db: Session, familia_id: int):
    familia = get_familia(db, familia_id)
    db.delete(familia)
    db.commit()
    return {"message": "Family deleted successfully"}

def update_familia(db: Session, familia_id: int, familia_data: dict):
    familia = get_familia(db, familia_id)
    if not familia:
        return None
    for key, value in familia_data.items():
        setattr(familia, key, value)
    db.commit()
    db.refresh(familia)
    return familia
