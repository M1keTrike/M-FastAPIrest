from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from ..db.database import Base

class Activity(Base):
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    priority = Column(Enum("alta", "media", "baja"), nullable=False)
    state = Column(Enum("pendiente", "en_progreso", "completada", "cancelada"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    categorY_id = Column(Integer, ForeignKey("categorias.id"))
