from fastapi import APIRouter
from app.api.v1.endpoints import ollama
from app.api.v1.endpoints import chat
from app.api.v1.endpoints import files

api_router = APIRouter()
api_router.include_router(ollama.router)
api_router.include_router(chat.router)
api_router.include_router(files.router)