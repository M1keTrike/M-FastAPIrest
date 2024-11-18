from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.pertenece_schema import PerteneceCreate, PerteneceResponse
from app.schemas.usuario_schema import Usuario
from app.controllers.pertenece_controller import (
    create_relationship,
    get_relationships_by_user,
    get_relationships_by_family,
    delete_relationship,
    get_users_by_family,
)
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=PerteneceResponse)
def create_relationship_route(relationship: PerteneceCreate, db: Session = Depends(get_db)):
    return create_relationship(db, relationship)


@router.get("/user/{user_id}", response_model=list[PerteneceResponse])
def read_relationships_by_user(user_id: int, db: Session = Depends(get_db)):
    return get_relationships_by_user(db, user_id)


@router.get("/family/{familia_id}", response_model=list[PerteneceResponse])
def read_relationships_by_family(familia_id: int, db: Session = Depends(get_db)):
    return get_relationships_by_family(db, familia_id)


@router.delete("/{relationship_id}")
def delete_relationship_route(relationship_id: int, db: Session = Depends(get_db)):
    return delete_relationship(db, relationship_id)


@router.get("/family/{familia_id}/users", response_model=list[Usuario])
def read_users_by_family(familia_id: int, db: Session = Depends(get_db)):
    return get_users_by_family(db, familia_id)
