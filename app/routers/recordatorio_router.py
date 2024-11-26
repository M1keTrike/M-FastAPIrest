from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.recordatorio_schema import NotificacionCreate, NotificacionResponse, NotificacionUpdate
from app.controllers.recordatorio_controller import (
    send_email,
    program_email,
    get_notificacion,
    get_notificaciones,
    delete_notificacion,
    update_notificacion,
    obtener_5_notificaciones_proximas,
    obtener_notificaciones_por_categoria_y_usuario
)
from datetime import datetime
from app.db.database import get_db
from app.utils.jwt_utils import get_current_user  # Importa la función get_current_user

router = APIRouter()

# Ruta pública para crear una notificación (sin autenticación)
@router.post("/")
def create_notificacion(
    notificacion: NotificacionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()  # Obtener la hora actual en UTC
    result = program_email(notificacion, db, now)
    return result

# Ruta protegida: Obtener una notificación por ID
@router.get("/{notificacion_id}", response_model=NotificacionResponse)
def read_notification(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Requiere autenticación
):
    notificacion = get_notificacion(db, notificacion_id)
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notificacion

# Ruta protegida: Obtener todas las notificaciones
@router.get("/", response_model=list[NotificacionResponse])
def read_notifications(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Requiere autenticación
):
    return get_notificaciones(db)

# Ruta protegida: Actualizar una notificación
@router.put("/{notificacion_id}", response_model=NotificacionUpdate)
def update_notification(
    notificacion_id: int,
    notificacion: NotificacionCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Requiere autenticación
):
    updated_notificacion = update_notificacion(db, notificacion_id, notificacion.dict())
    if updated_notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notificacion

# Ruta protegida: Eliminar una notificación
@router.delete("/{notificacion_id}")
def delete_notification(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Requiere autenticación
):
    return delete_notificacion(db, notificacion_id)

# Ruta protegida: Obtener próximas notificaciones de un usuario
@router.get("/proximas/{usuario_id}", response_model=list[NotificacionResponse])
def get_proximas_notificaciones(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Requiere autenticación
):
    notificaciones = obtener_5_notificaciones_proximas(db, usuario_id)
    if not notificaciones:
        raise HTTPException(status_code=404, detail="No se encontraron notificaciones")
    return notificaciones

# Ruta protegida: Obtener notificaciones por categoría y usuario
@router.get("/categoria/{categoria}/{usuario_id}", response_model=list[NotificacionResponse])
def get_notificaciones_por_categoria(
    categoria: str,
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)  # Requiere autenticación
):
    notificaciones = obtener_notificaciones_por_categoria_y_usuario(db, categoria, usuario_id)
    if not notificaciones:
        raise HTTPException(status_code=404, detail="No se encontraron notificaciones para esta categoría.")
    return notificaciones
