from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Familia(Base):
    __tablename__ = "familias"

    id_familia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
