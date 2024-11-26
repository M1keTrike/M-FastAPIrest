from typing import Optional
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: Optional[str]
    apellido_pat: Optional[str]
    apellido_mat: Optional[str]
    correo: Optional[EmailStr]
    contrasena: Optional[str]
    familia_id: Optional[int] = None
    imageid: Optional[str] = "6742890fa340d8718c911424"


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido_pat: Optional[str] = None
    apellido_mat: Optional[str] = None
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    familia_id: Optional[int] = None
    imageid: Optional[str] = "6742890fa340d8718c911424"


class Usuario(UsuarioBase):
    usuario_id: int


class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str

    class Config:
        from_attributes = True
