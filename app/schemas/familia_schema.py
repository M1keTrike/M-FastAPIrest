from pydantic import BaseModel

class FamiliaBase(BaseModel):
    nombre: str

class FamiliaCreate(FamiliaBase):
    pass

class Familia(FamiliaBase):
    id_familia: int

    class Config:
        orm_mode = True
