from fastapi import APIRouter
from app.api.v1.endpoints import ollama

api_router = APIRouter()
api_router.include_router(ollama.router)