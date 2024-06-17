from fastapi import FastAPI
from server.routes.map import router as map_router
from server.routes.card import router as card_router

app = FastAPI()
app.include_router(card_router, prefix="/cards", tags=["Cards"])
app.include_router(map_router, prefix="/maps", tags=["Maps"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}

