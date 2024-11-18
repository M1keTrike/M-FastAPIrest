from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    apellido_pat: str
    apellido_mat: str
    correo: EmailStr
    contrasena: str
    familia_id: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    pass


class Usuario(UsuarioBase):
    usuario_id: int

    class Config:
        from_attributes = True
