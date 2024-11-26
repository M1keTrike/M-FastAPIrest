from sqlalchemy import Column, Integer, Text, ForeignKey, String, DateTime,JSON
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.database import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"

    notificacion_id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)  # Nuevo campo para el título
    contenido = Column(Text, nullable=False)
    fecha_hora = Column(DateTime, nullable=False)  # Fecha y hora exacta de la notificación
    evento_id = Column(Integer, ForeignKey("eventos.evento_id"), nullable=True)  # Relación opcional con eventos
    familia_id = Column(Integer, ForeignKey("familias.id_familia"), nullable=True)  # Relación opcional con familias
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)  # Relación opcional con usuarios
    categoria = Column(String(50),nullable=False)
    correo_destinatario = Column(JSON, nullable=True)  # Correo destinatario como lista de correos electrónicos
