from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.models.familia_model import Familia
from app.schemas.usuario_schema import UsuarioCreate
from app.utils.jwt_utils import get_password_hash, verify_password
from sqlalchemy.exc import IntegrityError
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
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado en el sistema."
        )


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


def verify_user(db: Session, email: str, user_password: str):
    user = db.query(Usuario).filter(Usuario.correo == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(user_password, user.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    user_data = {
        "usuario_id": user.usuario_id,
        "nombre": user.nombre,
        "apellido_pat": user.apellido_pat,
        "apellido_mat": user.apellido_mat,
        "correo": user.correo,
        "rol": user.rol,
        "familia_id": user.familia_id
    }

    return {"message": "Login successful", "user": user_data}


def update_family_id(db: Session, user_id: int, familia_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    familia = db.query(Familia).filter(
        Familia.id_familia == familia_id).first()
    if not familia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family not found"
        )

    user.familia_id = familia_id
    db.commit()
    db.refresh(user)
    return user
