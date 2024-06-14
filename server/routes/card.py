
from typing import List
from fastapi import APIRouter, HTTPException
from server.models.card import CardSchema
from server.database import db

router = APIRouter()

@router.get("/", response_description="Cards retrieved", response_model=List[CardSchema])
async def get_all_cards():
    response = db.table("cards").select("*").execute()
    if response and len(response.data) > 0:
        return response.data

    raise HTTPException(status_code=404, detail="No cards found")

@router.get("/{id}", response_description="Card data retrieved", response_model=CardSchema)
async def get_card_id(id):
    response = db.table("cards").select("*").eq("id", id).execute()
    if response and len(response.data) > 0:
        return response.data[0]

    raise HTTPException(status_code=404, detail=f"Card {id} not found")

