from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.models.familia_model import Familia
from app.schemas.usuario_schema import UsuarioCreate
from app.utils.jwt_utils import get_password_hash
from fastapi import HTTPException, status


def create_user(db: Session, user_data: UsuarioCreate):
    hashed_password = get_password_hash(user_data.contrasena)
    db_user = Usuario(
        nombre=user_data.nombre,
        apellido_pat=user_data.apellido_pat,
        apellido_mat=user_data.apellido_mat,
        correo=user_data.correo,
        contrasena=hashed_password,
        rol=user_data.rol,
        familia_id=user_data.familia_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.usuario_id == user_id).first()


def get_users(db: Session):
    return db.query(Usuario).all()


def get_users_by_familia(db: Session, familia_id: int):
    return db.query(Usuario).filter(Usuario.familia_id == familia_id).all()


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def update_user(db: Session, user_id: int, user_data: dict):
    user = get_user(db, user_id)
    if not user:
        return None

    if "familia_id" in user_data and user_data["familia_id"] is not None:
        familia = db.query(Familia).filter(
            Familia.id_familia == user_data["familia_id"]).first()
        if not familia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family not found"
            )

    if "contrasena" in user_data:
        user_data["contrasena"] = get_password_hash(user_data["contrasena"])

    for key, value in user_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
