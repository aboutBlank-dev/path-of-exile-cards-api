
from typing import List
from fastapi import APIRouter, HTTPException
from server.models.card import CardSchema
from server.database import data_cache

router = APIRouter()

@router.get("/", response_description="Cards retrieved", response_model=List[CardSchema])
async def get_all_cards():
    data = data_cache.get_all_cards()
    if data:
        return data 

    raise HTTPException(status_code=404, detail="No cards found")

@router.get("/{id}", response_description="Card data retrieved", response_model=CardSchema)
async def get_card_id(id):
    data = data_cache.get_card_id(id)
    if data:
        return data

    raise HTTPException(status_code=404, detail=f"Card {id} not found")
