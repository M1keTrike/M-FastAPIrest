from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str]
    color: Optional[str]
    user_id: int 

class Category(BaseModel):
    id: int
    name: str
    description: Optional[str]
    color: Optional[str] 
    user_id: int 
