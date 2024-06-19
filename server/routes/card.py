
from typing import List
from fastapi import APIRouter, HTTPException, Query
from server.models.card import CardSchema
from server.database import data_cache

router = APIRouter()

@router.get("/", response_description="Cards retrieved", response_model=List[CardSchema])
async def get_cards(card_ids: List[str] = Query(None)):
    if(card_ids and len(card_ids) > 0):
        cards = data_cache.get_cards(card_ids)
        return cards
    else:
        cards = data_cache.get_all_cards()
        if cards:
            return cards

    raise HTTPException(status_code=404, detail="No cards found")

@router.get("/{id}", response_description="Card data retrieved", response_model=CardSchema)
async def get_card_id(id):
    data = data_cache.get_card_id(id)
    if data:
        return data

    raise HTTPException(status_code=404, detail=f"Card {id} not found")

@router.get("/drop_areas/{id}", response_model=List[str])
async def get_card_drop_areas(id):
    data = data_cache.get_card_id(id)
    if data and "drop_areas" in data:
        return data["drop_areas"]

    raise HTTPException(status_code=404, detail=f"Card {id} not found")