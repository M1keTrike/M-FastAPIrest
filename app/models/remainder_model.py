from sqlalchemy import Column, Integer, String, Enum, DateTime, Text, ForeignKey
from ..db.database import Base

class Remainder(Base):
    __tablename__ = "recordatorios"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    date_hour = Column(DateTime, nullable=False)
    repetition = Column(Enum("diaria", "semanal", "mensual", "anual", "ninguna"), default="ninguna")
    state = Column(Enum("activo", "inactivo"), default="activo")
    aditional_note = Column(Text)
    activity_id = Column(Integer, ForeignKey("actividades.id"))
