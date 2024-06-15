from typing import List, Optional
from pydantic import BaseModel, Field

class MapSchema(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    unique: bool = Field(...)
    alias: str = Field(...)
    cards: List[str] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "Map 1",
                "unique": True,
                "alias": "map1",
                "cards": ["Card_1", "Card_1"]
            }
        }
