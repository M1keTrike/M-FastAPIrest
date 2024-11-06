from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..db.database import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    creation_date = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
