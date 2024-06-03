from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Item(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    description: str
    price: float