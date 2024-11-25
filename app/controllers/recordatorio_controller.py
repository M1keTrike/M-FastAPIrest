from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.recordatorio_model import Notificacion
from app.schemas.recordatorio_schema import NotificacionCreate,NotificacionBase,NotificacionMail

import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()

email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")

def send_email(notificacion: NotificacionMail):
    # Create the email message
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = notificacion.correo_destinatario  # Send to the email provided in the request
    em["Subject"] = notificacion.titulo  # Use the title as the subject
    em.set_content(notificacion.contenido)  # The content of the email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, notificacion.correo_destinatario, em.as_string())

def create_notificacion(db: Session, notificacion_data: NotificacionCreate):
    
    db_notificacion = Notificacion(**notificacion_data.dict())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

def get_notificacion(db: Session, notificacion_id: int):
   
    return db.query(Notificacion).filter(Notificacion.notificacion_id == notificacion_id).first()

def get_notificaciones(db: Session):
    
    return db.query(Notificacion).all()

def delete_notificacion(db: Session, notificacion_id: int):
    
    notificacion = get_notificacion(db, notificacion_id)
    if notificacion:
        db.delete(notificacion)
        db.commit()
        return {"message": "Notification deleted successfully"}
    return {"message": "Notification not found"}

def update_notificacion(db: Session, notificacion_id: int, notificacion_data: dict):
    
    notificacion = get_notificacion(db, notificacion_id)
    if notificacion is None:
        return None
    for key, value in notificacion_data.items():
        setattr(notificacion, key, value)
    db.commit()
    db.refresh(notificacion)
    return notificacion

def obtener_5_notificaciones_proximas(db: Session, usuario_id: int):
    result = db.execute(text("SELECT * FROM obtener_5_notificaciones_proximas(:usuario_id)"), {"usuario_id": usuario_id})
    return result.fetchall()

def obtener_notificaciones_por_categoria_y_usuario(db: Session, categoria: str, usuario_id: int):
    query = text("""
        SELECT * FROM obtener_notificaciones_por_categoria_y_usuario(:categoria, :user_id) 
                 """)
    result = db.execute(query, {"categoria": categoria, "user_id": usuario_id})
    return result.fetchall()

