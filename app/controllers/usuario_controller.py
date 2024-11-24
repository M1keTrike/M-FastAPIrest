from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.models.pertenece_model import Pertenece
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
        imageid=user_data.imageid
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        if getattr(user_data, "familia_id", None):
            familia = db.query(Familia).filter(
                Familia.id_familia == user_data.familia_id).first()
            if not familia:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Family not found"
                )
            db_pertenece = Pertenece(
                usuario_id=db_user.usuario_id,
                familia_id=user_data.familia_id,
                rol="miembro"
            )
            db.add(db_pertenece)
            db.commit()
            db.refresh(db_pertenece)

        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado en el sistema."
        )


def get_user(db: Session, user_id: int):
    user = db.query(Usuario).filter(Usuario.usuario_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def get_users(db: Session):
    return db.query(Usuario).all()


def get_users_by_family(db: Session, familia_id: int):
    return (
        db.query(Usuario)
        .join(Pertenece, Usuario.usuario_id == Pertenece.usuario_id)
        .filter(Pertenece.familia_id == familia_id)
        .all()
    )


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.query(Pertenece).filter(
        Pertenece.usuario_id == user.usuario_id).delete()

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


def update_user(db: Session, user_id: int, user_data: dict):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if "familia_id" in user_data and user_data["familia_id"] is not None:
        familia = db.query(Familia).filter(
            Familia.id_familia == user_data["familia_id"]).first()
        if not familia:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family not found"
            )

        pertenece = (
            db.query(Pertenece)
            .filter(Pertenece.usuario_id == user.usuario_id, Pertenece.familia_id == user_data["familia_id"])
            .first()
        )
        if not pertenece:
            db_pertenece = Pertenece(
                usuario_id=user.usuario_id,
                familia_id=user_data["familia_id"],
                rol="miembro"
            )
            db.add(db_pertenece)
            db.commit()
            db.refresh(db_pertenece)

    if "contrasena" in user_data and user_data["contrasena"]:
        user_data["contrasena"] = get_password_hash(user_data["contrasena"])

    for key, value in user_data.items():
        if key != "familia_id" and value is not None:
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

    roles = (
        db.query(Pertenece)
        .filter(Pertenece.usuario_id == user.usuario_id)
        .all()
    )

    user_data = {
        "usuario_id": user.usuario_id,
        "nombre": user.nombre,
        "apellido_pat": user.apellido_pat,
        "apellido_mat": user.apellido_mat,
        "correo": user.correo,
        "roles": [{"familia_id": r.familia_id, "rol": r.rol} for r in roles],
    }

    return {"message": "Login successful", "user": user_data}


def get_user_with_roles(db: Session, user_id: int):
    user = db.query(Usuario).filter(Usuario.usuario_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    roles = (
        db.query(Pertenece)
        .filter(Pertenece.usuario_id == user_id)
        .all()
    )

    user_data = {
        "usuario_id": user.usuario_id,
        "nombre": user.nombre,
        "apellido_pat": user.apellido_pat,
        "apellido_mat": user.apellido_mat,
        "correo": user.correo,
        "roles": [{"familia_id": r.familia_id, "rol": r.rol} for r in roles],
    }

    return user_data
