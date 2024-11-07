from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido_pat = Column(String(50), nullable=False)
    apellido_mat = Column(String(50))
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    rol = Column(String(50))
    familia_id = Column(Integer)
