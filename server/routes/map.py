from typing import List
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from server.models.map import MapSchema
from server.database import db

router = APIRouter()

@router.get("/", response_model=List[MapSchema])
async def get_all_maps():
    response = db.table("maps").select("*").execute()
    if response and len(response.data) > 0:
        return response.data

    raise HTTPException(status_code=404, detail="No maps found")

@router.get("/{id}", response_model=MapSchema)
async def get_map_id(id):
    response = db.table("maps").select("*").eq("id", id).execute()
    if response and len(response.data) > 0:
        return response.data[0]
    
    raise HTTPException(status_code=404, detail=f"Map with id: {id} not found")