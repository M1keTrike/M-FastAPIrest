from sqlalchemy.orm import Session
from app.models.pertenece_model import Pertenece
from app.models.usuario_model import Usuario
from app.models.familia_model import Familia
from app.schemas.pertenece_schema import PerteneceCreate, PerteneceResponse
from fastapi import HTTPException, status


def create_relationship(db: Session, relationship_data: PerteneceCreate):
    usuario = db.query(Usuario).filter(Usuario.usuario_id == relationship_data.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if relationship_data.familia_id:
        familia = db.query(Familia).filter(Familia.id_familia == relationship_data.familia_id).first()
        if not familia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family not found")

    db_relationship = Pertenece(
        usuario_id=relationship_data.usuario_id,
        familia_id=relationship_data.familia_id,
        rol=relationship_data.rol,
    )
    db.add(db_relationship)
    db.commit()
    db.refresh(db_relationship)
    return PerteneceResponse.from_orm(db_relationship)


def get_relationships_by_user(db: Session, usuario_id: int):
    relationships = db.query(Pertenece).filter(Pertenece.usuario_id == usuario_id).all()
    if not relationships:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No relationships found for user")
    return [PerteneceResponse.from_orm(r) for r in relationships]


def get_relationships_by_family(db: Session, familia_id: int):
    relationships = db.query(Pertenece).filter(Pertenece.familia_id == familia_id).all()
    if not relationships:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No relationships found for family")
    return [PerteneceResponse.from_orm(r) for r in relationships]


def delete_relationship(db: Session, relationship_id: int):
    relationship = db.query(Pertenece).filter(Pertenece.id == relationship_id).first()
    if not relationship:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relationship not found")

    db.delete(relationship)
    db.commit()
    return {"message": "Relationship deleted successfully"}


def get_users_by_family(db: Session, familia_id: int):
    familia = db.query(Familia).filter(Familia.id_familia == familia_id).first()
    if not familia:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family not found")

    users = (
        db.query(Usuario)
        .join(Pertenece, Usuario.usuario_id == Pertenece.usuario_id)
        .filter(Pertenece.familia_id == familia_id)
        .all()
    )
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found for the family")
    return users
