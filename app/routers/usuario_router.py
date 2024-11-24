from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioBase, UsuarioCreate, Usuario
from app.schemas.usuario_schema import UsuarioUpdate
from app.controllers.usuario_controller import (
    create_user,
    get_user,
    get_users,
    delete_user,
    update_user,
    verify_user,
    get_user_with_roles
)
from app.db.database import get_db

router = APIRouter()


@router.post("/register", response_model=Usuario)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.post("/login")
def login(email: str, user_password: str, db: Session = Depends(get_db)):
    return verify_user(db, email, user_password)


@router.get("/{user_id}", response_model=Usuario)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[Usuario])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.put("/{user_id}", response_model=Usuario)
def update_user_route(user_id: int, user: UsuarioUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user.dict(exclude_unset=True))
    return updated_user


@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


@router.get("/roles/{user_id}")
def read_user_with_roles(user_id: int, db: Session = Depends(get_db)):
    user_data = get_user_with_roles(db, user_id)
    return user_data
