from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.controllers.pertenece_controller import create_relationship, get_relationships_by_user
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
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        if user_data.familia_id:
            create_relationship(db, {
                "usuario_id": db_user.usuario_id,
                "familia_id": user_data.familia_id,
                "rol": "miembro" 
            })

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


def get_users_by_family(db: Session, familia_id: int):
    from app.controllers.pertenece_controller import get_relationships_by_family

    relationships = get_relationships_by_family(db, familia_id)
    user_ids = [relationship.usuario_id for relationship in relationships]
    return db.query(Usuario).filter(Usuario.usuario_id.in_(user_ids)).all()


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

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
        from app.controllers.pertenece_controller import create_relationship

        create_relationship(db, {
            "usuario_id": user_id,
            "familia_id": user_data["familia_id"],
            "rol": "miembro"
        })

    if "contrasena" in user_data:
        user_data["contrasena"] = get_password_hash(user_data["contrasena"])

    for key, value in user_data.items():
        if key not in ["familia_id", "rol"]:
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

    roles = get_relationships_by_user(db, user.usuario_id)

    user_data = {
        "usuario_id": user.usuario_id,
        "nombre": user.nombre,
        "apellido_pat": user.apellido_pat,
        "apellido_mat": user.apellido_mat,
        "correo": user.correo,
        "roles": [{"familia_id": r.familia_id, "rol": r.rol} for r in roles],
    }

    return {"message": "Login successful", "user": user_data}
