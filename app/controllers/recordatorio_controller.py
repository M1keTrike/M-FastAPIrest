from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
import pytz  

from app.models.recordatorio_model import Notificacion
from app.schemas.recordatorio_schema import NotificacionCreate,NotificacionBase,NotificacionMail

import os
import ssl
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
scheduler = BackgroundScheduler()
scheduler.start()

email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")

def send_email(notificacion: NotificacionMail):
    """Función para enviar un correo electrónico a uno o varios destinatarios."""
    if not notificacion.correo_destinatario:
        raise ValueError("Se requiere al menos un destinatario para enviar el correo.")

    # Configuración de conexión segura
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        # Enviar un correo por cada destinatario
        for correo in notificacion.correo_destinatario:
            # Crear un nuevo mensaje para cada destinatario
            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = correo
            em["Subject"] = notificacion.titulo
            em.set_content(notificacion.contenido)

            # Enviar el correo
            smtp.sendmail(email_sender, correo, em.as_string())


def program_email(notificacion: NotificacionMail, now: datetime):
    """Programa o envía un correo inmediatamente según la fecha indicada."""
    # Convertir la fecha de entrada a UTC (aware)
    if not notificacion.fecha_hora.tzinfo:
        notificacion.fecha_hora = pytz.UTC.localize(notificacion.fecha_hora)

    # Asegúrate de que la fecha actual también esté en UTC
    if not now.tzinfo:
        now = pytz.UTC.localize(now)

    delay = (notificacion.fecha_hora - now).total_seconds()

    if delay > 0:
        # Programar el correo para el futuro
        scheduler.add_job(
            send_email,
            'date',
            run_date=notificacion.fecha_hora,
            args=[notificacion]
        )
        return "Correo programado exitosamente."
    else:
        # Enviar el correo de inmediato
        send_email(notificacion)
        return "La fecha ya pasó, el correo se envió de inmediato."

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

