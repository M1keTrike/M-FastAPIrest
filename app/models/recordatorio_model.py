from sqlalchemy import Column, Integer, Text, Time, ForeignKey
from app.db.database import Base

class Recordatorio(Base):
    __tablename__ = "recordatorios"

    recordatorio_id = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text, nullable=False)
    id_familia = Column(Integer, ForeignKey("familias.id_familia"))
    hora_limite = Column(Time)
