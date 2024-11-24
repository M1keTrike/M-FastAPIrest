from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido_pat = Column(String(50), nullable=False)
    apellido_mat = Column(String(50))
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    imageid = Column(String(50), nullable=False, default="6742890fa340d8718c911424")  

    pertenencias = relationship("Pertenece", back_populates="usuario", cascade="all, delete-orphan")
