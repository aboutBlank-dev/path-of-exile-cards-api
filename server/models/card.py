from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class CardSchema(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    drop_areas: list = Field(...) # List of strings (map ids)
    stack_size: int = Field(...)
    reward_text: Optional[dict] = Field({})
    chaos_value: float = Field(...)
    divine_value: float = Field(...)
    art_url: str = Field(...)
    alias: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra= {
            "example": {
                "id": "card_1",
                "name": "Card 1",
                "drop_areas": ["Area_id_1", "area_id_2"],
                "stack_size": 1,
                "reward_text": {"reward": "reward text"},
                "chaos_value": 1.0,
                "divine_value": 1.0,
                "art_url": "https://www.example.com/image.jpg",
                "alias": "card"
            }
        }
    )
