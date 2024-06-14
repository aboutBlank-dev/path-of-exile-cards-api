from fastapi import FastAPI
from server.models.card import CardSchema
from server.routes.map import router as map_router
from server.routes.card import router as card_router
from server.database import db

app = FastAPI()
app.include_router(card_router, prefix="/card", tags=["Card"])
app.include_router(map_router, prefix="/map", tags=["Map"])

@app.get("/")
def read_root():
    test_map = {
        "id": "1",
        "name": "Map 1",
        "description": "Map 1 description",
        "image": "https://www.example.com/image.jpg",
        "is_active": True
    }
    db.table("maps").insert(test_map).execute()
    return {"message": "Hello World"}