from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.recordatorio_schema import NotificacionCreate, NotificacionBase,Notificacion,NotificacionMail
from app.controllers.recordatorio_controller import send_email,create_notificacion, get_notificacion, get_notificaciones, delete_notificacion, update_notificacion,obtener_5_notificaciones_proximas, obtener_notificaciones_por_categoria_y_usuario
from app.db.database import get_db




router = APIRouter()

@router.post("/send_email/")
async def send_email_route(notificacion: NotificacionMail):
    try:
        send_email(notificacion)
        return {"message": "Email sent successfully to " + notificacion.correo_destinatario}
    except Exception as e:
        return {"error": str(e)}

@router.post("/", response_model=Notificacion)
def create_notification(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    return create_notificacion(db, notificacion)

@router.get("/{notificacion_id}", response_model=Notificacion)
def read_notification(notificacion_id: int, db: Session = Depends(get_db)):
    notificacion = get_notificacion(db, notificacion_id)
    if notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notificacion

@router.get("/", response_model=list[Notificacion])
def read_notifications(db: Session = Depends(get_db)):
    return get_notificaciones(db)

@router.put("/{notificacion_id}", response_model=Notificacion)
def update_notification(notificacion_id: int, notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    updated_notificacion = update_notificacion(db, notificacion_id, notificacion.dict())
    if updated_notificacion is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notificacion

@router.delete("/{notificacion_id}")
def delete_notification(notificacion_id: int, db: Session = Depends(get_db)):
    return delete_notificacion(db, notificacion_id)

@router.get("/proximas/{usuario_id}", response_model=list[Notificacion])
def get_proximas_notificaciones(usuario_id: int, db: Session = Depends(get_db)):
    notificaciones = obtener_5_notificaciones_proximas(db, usuario_id)
    
    if not notificaciones:
        raise HTTPException(status_code=404, detail="No se encontraron notificaciones")
    
    return notificaciones
@router.get("/categoria/{categoria}/{usuario_id}", response_model=list[Notificacion])
def get_notificaciones_por_categoria(categoria: str, usuario_id: int, db: Session = Depends(get_db)):
    notificaciones = obtener_notificaciones_por_categoria_y_usuario(db, categoria,usuario_id)
    if not notificaciones:
        raise HTTPException(status_code=404, detail="No se encontraron notificaciones para esta categoría.")
    return notificaciones

