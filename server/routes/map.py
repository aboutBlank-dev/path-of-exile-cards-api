from typing import List
from fastapi import APIRouter, Body, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from server.models.map import MapSchema
from server.database import data_cache

router = APIRouter()

@router.get("/", response_model=List[MapSchema])
async def get_maps(map_ids: List[str] = Query(None)):
    if map_ids and len(map_ids) > 0: 
        maps = data_cache.get_maps(map_ids)
        return maps
    else:
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

@router.get("/drop_cards/{id}", response_model=List[str])
def get_map_drop_cards(id):
    map = data_cache.get_map_id(id)
    if map and "cards" in map:
        return map["cards"]
    
    raise HTTPException(status_code=404, detail=f"Map with id: {id} not found")
