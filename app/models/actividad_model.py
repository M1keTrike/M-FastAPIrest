from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from app.db.database import Base

class Actividad(Base):
    __tablename__ = "actividades"

    actividad_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    fecha_fin = Column(Date)
    hora_fin = Column(Time)
    categoria = Column(String(50))
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)  

