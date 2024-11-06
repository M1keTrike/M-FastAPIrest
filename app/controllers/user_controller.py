from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import Usuario
from app.schemas.user_schema import UsuarioCreate
from app.utils.jwt_utils import get_password_hash, verify_password

def create_user(db: Session, user_data: UsuarioCreate):
    hashed_password = get_password_hash(user_data.contrasena)
    db_user = Usuario(nombre_usuario=user_data.nombre_usuario, correo=user_data.correo, contraseña=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully", "user": db_user}

def login_user(db: Session, user_data: UsuarioCreate):
    db_user = db.query(Usuario).filter(Usuario.correo == user_data.correo).first()
    if not db_user or not verify_password(user_data.contrasena, db_user.contraseña):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful", "user": {"nombre_usuario": db_user.nombre_usuario, "correo": db_user.correo}}

def get_users(db: Session):
    return db.query(Usuario).all()

def get_user(db: Session, usuario_id: int):
    user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
