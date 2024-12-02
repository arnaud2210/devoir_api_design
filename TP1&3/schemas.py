from pydantic import BaseModel
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: str | None = None
    author: str | None = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True
