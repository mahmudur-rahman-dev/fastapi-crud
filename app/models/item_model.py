from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Item(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str
    description: str
    price: float

    # class Config:
    #     allow_population_by_field_name = True
    #     json_encoders = {
    #         ObjectId: str
    #     }
    #     arbitrary_types_allowed = True
    #     alias_generator = lambda s: s
    #     allow_population_by_alias = True