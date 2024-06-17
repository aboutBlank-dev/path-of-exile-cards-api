from typing import List
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from server.models.map import MapSchema
from server.database import data_cache

router = APIRouter()

@router.get("/", response_model=List[MapSchema])
async def get_all_maps():
    maps = data_cache.get_all_maps()
    if maps:
        return maps

    raise HTTPException(status_code=404, detail="No maps found")

@router.get("/{id}", response_model=MapSchema)
async def get_map_id(id):
    map = data_cache.get_map_id(id)
    if map:
        return map
    
    raise HTTPException(status_code=404, detail=f"Map with id: {id} not found")