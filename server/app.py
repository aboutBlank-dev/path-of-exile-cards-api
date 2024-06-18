from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.card import router as card_router
from server.routes.map import router as map_router

app = FastAPI()
origins = ["0.0.0.0"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])
app.include_router(card_router, prefix="/cards", tags=["Cards"])
app.include_router(map_router, prefix="/maps", tags=["Maps"])

