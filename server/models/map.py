from typing import Optional
from pydantic import BaseModel, Field

class MapSchema(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    image: str = Field(...)
    is_active: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "Map 1",
                "description": "Map 1 description",
                "image": "https://www.example.com/image.jpg",
                "is_active": True
            }
        }
