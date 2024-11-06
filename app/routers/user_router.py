from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UsuarioCreate, Usuario
from app.controllers.user_controller import create_user, login_user, get_user, get_users

router = APIRouter()

@router.post("/register", response_model=UsuarioCreate)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login")
def login(user: UsuarioCreate, db: Session = Depends(get_db)):
    return login_user(db, user)

@router.get("/", response_model=list[Usuario])  
def read_users(db: Session = Depends(get_db)):
    return get_users(db)

@router.get("/{usuario_id}", response_model=Usuario)  
def read_user(usuario_id: int, db: Session = Depends(get_db)):
    return get_user(db, usuario_id)
