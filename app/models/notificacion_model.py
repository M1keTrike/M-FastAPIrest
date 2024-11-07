from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from app.db.database import Base

class Notificacion(Base):
    __tablename__ = "notificaciones"

    notificacion_id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.evento_id"))
    mensaje = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
