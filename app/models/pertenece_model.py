from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum


class RolEnum(enum.Enum):
    miembro = "miembro"
    lider = "lider"


class Pertenece(Base):
    __tablename__ = "pertenece"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey(
        "usuarios.usuario_id", ondelete="CASCADE"), nullable=False)
    familia_id = Column(Integer, ForeignKey(
        "familias.id_familia", ondelete="SET NULL"), nullable=True)
    rol = Column(Enum(RolEnum), nullable=False)

    usuario = relationship("Usuario", back_populates="pertenencias")
    familia = relationship("Familia", back_populates="miembros")
