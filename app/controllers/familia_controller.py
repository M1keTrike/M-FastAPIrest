from sqlalchemy.orm import Session
from app.models.familia_model import Familia
from app.schemas.familia_schema import FamiliaCreate
from fastapi import HTTPException, status


def create_familia(db: Session, familia_data: FamiliaCreate):
    try:
        db_familia = Familia(**familia_data.dict())
        db.add(db_familia)
        db.commit()
        db.refresh(db_familia)
        return db_familia
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating family: {str(e)}"
        )


def get_familia(db: Session, familia_id: int):
    familia = db.query(Familia).filter(Familia.id_familia == familia_id).first()
    if not familia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Family with id {familia_id} not found"
        )
    return familia


def get_familias(db: Session):
    try:
        familias = db.query(Familia).all()
        return familias
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving families: {str(e)}"
        )


def delete_familia(db: Session, familia_id: int):
    familia = get_familia(db, familia_id)
    if not familia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Family with id {familia_id} not found"
        )
    try:
        db.delete(familia)
        db.commit()
        return {"message": "Family deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting family: {str(e)}"
        )


def update_familia(db: Session, familia_id: int, familia_data: dict):
    familia = get_familia(db, familia_id)
    if not familia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Family with id {familia_id} not found"
        )
    try:
        for key, value in familia_data.items():
            setattr(familia, key, value)
        db.commit()
        db.refresh(familia)
        return familia
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating family: {str(e)}"
        )
