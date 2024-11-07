from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.db.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    evento_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    familia_id = Column(Integer, ForeignKey("familias.id_familia"))
