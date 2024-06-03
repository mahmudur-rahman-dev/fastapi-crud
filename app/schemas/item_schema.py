from pydantic import BaseModel, Field
from typing import Optional

class ItemCreateSchema(BaseModel):
    name: str
    description: str
    price: float

class ItemResponseSchema(BaseModel):
    # id: Optional[str] = Field(None, alias="_id")
    id: str = Field(alias="id")
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True
