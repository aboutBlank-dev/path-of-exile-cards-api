from fastapi import FastAPI
from retrieve_map_card_data import get_map_card_data
from server.models.card import CardSchema
from server.models.map import MapSchema
from server.routes.map import router as map_router
from server.routes.card import router as card_router

app = FastAPI()
app.include_router(card_router, prefix="/card", tags=["Card"])
app.include_router(map_router, prefix="/map", tags=["Map"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}

