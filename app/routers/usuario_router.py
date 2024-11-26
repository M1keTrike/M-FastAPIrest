from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioBase, UsuarioCreate, Usuario, UsuarioLogin, UsuarioUpdate
from app.controllers.usuario_controller import (
    create_user,
    get_user,
    get_users,
    delete_user,
    update_user,
    verify_user,
    get_user_with_roles, login_user
)
from app.db.database import get_db
# Importa la función get_current_user
from app.utils.jwt_utils import get_current_user

router = APIRouter()

# Ruta pública para registro (sin autenticación)


@router.post("/register", response_model=Usuario)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

# Ruta pública para login (sin autenticación)


@router.post("/login")
def login(user_data: UsuarioLogin, db: Session = Depends(get_db)):
    return login_user(db=db, user_data=user_data)

# Proteger la ruta de obtener un usuario por su ID


@router.get("/{user_id}", response_model=Usuario)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Proteger la ruta de obtener todos los usuarios


@router.get("/", response_model=list[Usuario])
def read_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_users(db)

# Proteger la ruta de actualizar un usuario


@router.put("/{user_id}", response_model=Usuario)
def update_user_route(user_id: int, user: UsuarioUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    updated_user = update_user(db, user_id, user.dict(exclude_unset=True))
    return updated_user

# Proteger la ruta de eliminar un usuario


@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return delete_user(db, user_id)

# Proteger la ruta de obtener un usuario con sus roles


@router.get("/roles/{user_id}")
def read_user_with_roles(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user_data = get_user_with_roles(db, user_id)
    return user_data
