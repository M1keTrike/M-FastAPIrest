from sqlalchemy import Column, Integer, String, Text, ForeignKey
from ..db.database import Base

class Category(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    color = Column(String(7))
    user_id = Column(Integer, ForeignKey("usuarios.id"))
